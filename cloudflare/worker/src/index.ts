interface Env {
  INSTALLATIONS: D1Database;
  PORTRAITS: R2Bucket;
  PUBLIC_BASE_URL: string;
}

interface RegisterRequestBody {
  discord_application_id?: unknown;
  discord_bot_token?: unknown;
}

interface DiscordApplication {
  id?: string;
  name?: string;
}

interface InstallationRow {
  discord_application_id: string;
  token_hash: string;
  created_at: string;
  last_upload_at: string | null;
  is_enabled: number;
}

const DISCORD_API_BASE_URL = "https://discord.com/api/v10";

const MAX_PORTRAIT_SIZE_BYTES = 5 * 1024 * 1024;
const PNG_CONTENT_TYPE = "image/png";

function jsonResponse(
  body: unknown,
  status = 200,
): Response {
  return Response.json(body, {
    status,
    headers: {
      "Cache-Control": "no-store",
      "Content-Type": "application/json",
    },
  });
}

function isNumericId(value: string): boolean {
  return /^\d+$/.test(value);
}

function bytesToHex(bytes: ArrayBuffer): string {
  return Array.from(new Uint8Array(bytes))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function bytesToBase64Url(bytes: Uint8Array): string {
  let binary = "";

  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }

  return btoa(binary)
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/g, "");
}

function generateInstallToken(): string {
  const randomBytes = new Uint8Array(48);
  crypto.getRandomValues(randomBytes);

  return bytesToBase64Url(randomBytes);
}

async function hashToken(token: string): Promise<string> {
  const encodedToken = new TextEncoder().encode(token);

  const digest = await crypto.subtle.digest(
    "SHA-256",
    encodedToken,
  );

  return bytesToHex(digest);
}

function constantTimeEqual(
  firstValue: string,
  secondValue: string,
): boolean {
  if (firstValue.length !== secondValue.length) {
    return false;
  }

  let difference = 0;

  for (let index = 0; index < firstValue.length; index += 1) {
    difference |= (
      firstValue.charCodeAt(index)
      ^ secondValue.charCodeAt(index)
    );
  }

  return difference === 0;
}

function getBearerToken(request: Request): string {
  const authorization = (
    request.headers.get("Authorization")
    || ""
  ).trim();

  const prefix = "Bearer ";

  if (!authorization.startsWith(prefix)) {
    return "";
  }

  return authorization
    .slice(prefix.length)
    .trim();
}

function hasPngSignature(bytes: ArrayBuffer): boolean {
  const data = new Uint8Array(bytes);

  const signature = [
    0x89,
    0x50,
    0x4e,
    0x47,
    0x0d,
    0x0a,
    0x1a,
    0x0a,
  ];

  if (data.length < signature.length) {
    return false;
  }

  return signature.every(
    (value, index) => data[index] === value,
  );
}

async function readJsonBody(
  request: Request,
): Promise<RegisterRequestBody> {
  const contentType = (
    request.headers.get("Content-Type")
    || ""
  ).split(";")[0].trim().toLowerCase();

  if (contentType !== "application/json") {
    throw new Error(
      "Content-Type must be application/json.",
    );
  }

  try {
    return await request.json<RegisterRequestBody>();
  } catch {
    throw new Error(
      "Request body must contain valid JSON.",
    );
  }
}

async function verifyDiscordApplication(
  applicationId: string,
  botToken: string,
): Promise<DiscordApplication> {
  const response = await fetch(
    `${DISCORD_API_BASE_URL}/applications/@me`,
    {
      method: "GET",
      headers: {
        "Authorization": `Bot ${botToken}`,
        "User-Agent": (
          "DiscordBot (https://github.com/solxvt/WoWidget, 1.0.0)"
        ),
      },
    },
  );

  if (response.status === 401) {
    throw new Error(
      "Discord rejected the supplied bot token.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Discord validation failed with status ${response.status}.`,
    );
  }

  const application = (
    await response.json()
  ) as DiscordApplication;

  if (
    String(application.id || "")
    !== applicationId
  ) {
    throw new Error(
      "The supplied bot token does not belong to "
      + "the supplied Discord Application ID.",
    );
  }

  return application;
}

async function handleRegister(
  request: Request,
  env: Env,
): Promise<Response> {
  let body: RegisterRequestBody;

  try {
    body = await readJsonBody(request);
  } catch (error) {
    const message = (
      error instanceof Error
        ? error.message
        : "Invalid request body."
    );

    return jsonResponse(
      {
        success: false,
        error: message,
      },
      400,
    );
  }

  const applicationId = String(
    body.discord_application_id || "",
  ).trim();

  const botToken = String(
    body.discord_bot_token || "",
  ).trim();

  if (!isNumericId(applicationId)) {
    return jsonResponse(
      {
        success: false,
        error: (
          "A valid Discord Application ID is required."
        ),
      },
      400,
    );
  }

  if (!botToken) {
    return jsonResponse(
      {
        success: false,
        error: "A Discord bot token is required.",
      },
      400,
    );
  }

  let discordApplication: DiscordApplication;

  try {
    discordApplication = await verifyDiscordApplication(
      applicationId,
      botToken,
    );
  } catch (error) {
    const message = (
      error instanceof Error
        ? error.message
        : "Discord application verification failed."
    );

    return jsonResponse(
      {
        success: false,
        error: message,
      },
      401,
    );
  }

  const installToken = generateInstallToken();
  const tokenHash = await hashToken(installToken);
  const createdAt = new Date().toISOString();

  try {
    await env.INSTALLATIONS
      .prepare(
        `
        INSERT INTO installations (
          discord_application_id,
          token_hash,
          created_at,
          last_upload_at,
          is_enabled
        )
        VALUES (?, ?, ?, NULL, 1)
        ON CONFLICT(discord_application_id)
        DO UPDATE SET
          token_hash = excluded.token_hash,
          created_at = excluded.created_at,
          last_upload_at = NULL,
          is_enabled = 1
        `,
      )
      .bind(
        applicationId,
        tokenHash,
        createdAt,
      )
      .run();
  } catch (error) {
    console.error(
      "Unable to save installation registration.",
      error,
    );

    return jsonResponse(
      {
        success: false,
        error: (
          "Unable to create the WoWidget installation."
        ),
      },
      500,
    );
  }

  return jsonResponse(
    {
      success: true,
      discord_application_id: applicationId,
      discord_application_name: (
        discordApplication.name
        || "Discord application"
      ),
      install_token: installToken,
      created_at: createdAt,
    },
    201,
  );
}

async function handlePortraitUpload(
  request: Request,
  env: Env,
): Promise<Response> {
  const applicationId = (
    request.headers.get(
      "X-WoWidget-Application-Id",
    )
    || ""
  ).trim();

  const characterId = (
    request.headers.get(
      "X-WoWidget-Character-Id",
    )
    || ""
  ).trim();

  const installToken = getBearerToken(request);

  if (!isNumericId(applicationId)) {
    return jsonResponse(
      {
        success: false,
        error: (
          "A valid Discord Application ID is required."
        ),
      },
      400,
    );
  }

  if (!isNumericId(characterId)) {
    return jsonResponse(
      {
        success: false,
        error: (
          "A valid Blizzard character ID is required."
        ),
      },
      400,
    );
  }

  if (!installToken) {
    return jsonResponse(
      {
        success: false,
        error: "Installation authentication is required.",
      },
      401,
    );
  }

  const contentType = (
    request.headers.get("Content-Type")
    || ""
  ).split(";")[0].trim().toLowerCase();

  if (contentType !== PNG_CONTENT_TYPE) {
    return jsonResponse(
      {
        success: false,
        error: "Only PNG portrait uploads are accepted.",
      },
      415,
    );
  }

  let installation: InstallationRow | null;

  try {
    installation = await env.INSTALLATIONS
      .prepare(
        `
        SELECT
          discord_application_id,
          token_hash,
          created_at,
          last_upload_at,
          is_enabled
        FROM installations
        WHERE discord_application_id = ?
        LIMIT 1
        `,
      )
      .bind(applicationId)
      .first<InstallationRow>();
  } catch (error) {
    console.error(
      "Unable to read installation registration.",
      error,
    );

    return jsonResponse(
      {
        success: false,
        error: "Unable to verify this installation.",
      },
      500,
    );
  }

  if (!installation) {
    return jsonResponse(
      {
        success: false,
        error: "This WoWidget installation is not registered.",
      },
      401,
    );
  }

  if (installation.is_enabled !== 1) {
    return jsonResponse(
      {
        success: false,
        error: "This WoWidget installation is disabled.",
      },
      403,
    );
  }

  const suppliedTokenHash = await hashToken(
    installToken,
  );

  if (
    !constantTimeEqual(
      suppliedTokenHash,
      installation.token_hash,
    )
  ) {
    return jsonResponse(
      {
        success: false,
        error: "Invalid installation token.",
      },
      401,
    );
  }

  const contentLength = Number(
    request.headers.get("Content-Length") || "0",
  );

  if (
    Number.isFinite(contentLength)
    && contentLength > MAX_PORTRAIT_SIZE_BYTES
  ) {
    return jsonResponse(
      {
        success: false,
        error: "The portrait exceeds the 5 MB limit.",
      },
      413,
    );
  }

  const imageBytes = await request.arrayBuffer();

  if (imageBytes.byteLength === 0) {
    return jsonResponse(
      {
        success: false,
        error: "The uploaded portrait is empty.",
      },
      400,
    );
  }

  if (
    imageBytes.byteLength
    > MAX_PORTRAIT_SIZE_BYTES
  ) {
    return jsonResponse(
      {
        success: false,
        error: "The portrait exceeds the 5 MB limit.",
      },
      413,
    );
  }

  if (!hasPngSignature(imageBytes)) {
    return jsonResponse(
      {
        success: false,
        error: "The uploaded file is not a valid PNG.",
      },
      415,
    );
  }

  const objectKey = (
    `characters/${applicationId}/${characterId}.png`
  );

  const uploadedAt = new Date().toISOString();

  try {
    await env.PORTRAITS.put(
      objectKey,
      imageBytes,
      {
        httpMetadata: {
          contentType: PNG_CONTENT_TYPE,
          cacheControl: (
            "public, max-age=31536000, immutable"
          ),
        },
        customMetadata: {
          discordApplicationId: applicationId,
          characterId,
          uploadedAt,
        },
      },
    );

    await env.INSTALLATIONS
      .prepare(
        `
        UPDATE installations
        SET last_upload_at = ?
        WHERE discord_application_id = ?
        `,
      )
      .bind(
        uploadedAt,
        applicationId,
      )
      .run();
  } catch (error) {
    console.error(
      "Unable to upload portrait.",
      error,
    );

    return jsonResponse(
      {
        success: false,
        error: "Unable to store the character portrait.",
      },
      500,
    );
  }

  const publicBaseUrl = (
    env.PUBLIC_BASE_URL
      .replace(/\/+$/, "")
  );

  const version = Date.now();

  const publicUrl = (
    `${publicBaseUrl}/${objectKey}`
    + `?v=${version}`
  );

  return jsonResponse(
    {
      success: true,
      discord_application_id: applicationId,
      character_id: characterId,
      object_key: objectKey,
      public_url: publicUrl,
      size_bytes: imageBytes.byteLength,
      uploaded_at: uploadedAt,
    },
    201,
  );
}

export default {
  async fetch(
    request: Request,
    env: Env,
  ): Promise<Response> {
    const url = new URL(request.url);

    if (
      request.method === "GET"
      && url.pathname === "/health"
    ) {
      return jsonResponse({
        success: true,
        service: "WoWidget portrait uploader",
        bindings: {
          d1: Boolean(env.INSTALLATIONS),
          r2: Boolean(env.PORTRAITS),
          public_base_url: Boolean(
            env.PUBLIC_BASE_URL,
          ),
        },
      });
    }

    if (
      request.method === "POST"
      && url.pathname === "/register"
    ) {
      return handleRegister(
        request,
        env,
      );
    }

    if (
      request.method === "PUT"
      && url.pathname === "/portrait"
    ) {
      return handlePortraitUpload(
        request,
        env,
      );
    }

    return jsonResponse(
      {
        success: false,
        error: "Not found.",
      },
      404,
    );
  },
} satisfies ExportedHandler<Env>;