---
hide:
  - navigation
  - toc
---

<div class="support-hero">
  <p class="support-hero__eyebrow">WoWidget Support</p>
  <h1>Troubleshooting</h1>
  <p class="support-hero__summary">
    Find the symptom or error message you are seeing, then expand it for the most likely cause and the exact steps to resolve it.
  </p>
</div>

<div class="support-search" role="search">
  <div class="support-search__field">
    <span aria-hidden="true">⌕</span>
    <input
      id="troubleshooting-search"
      type="search"
      placeholder="Search errors, symptoms, or features…"
      aria-label="Search troubleshooting articles"
      autocomplete="off"
    >
    <button id="troubleshooting-clear" type="button" hidden>Clear</button>
  </div>
  <p id="troubleshooting-results" class="support-search__status" aria-live="polite"></p>
</div>

<nav class="support-categories" aria-label="Troubleshooting categories">
  <a href="#installation">Installation</a>
  <a href="#blizzard">Blizzard</a>
  <a href="#discord">Discord</a>
  <a href="#widget-editor">Widget Editor</a>
  <a href="#application">WoWidget App</a>
  <a href="#advanced">Advanced</a>
</nav>

<div class="ww-callout ww-callout--tip support-quick-check">
  <strong>Start with the quick checks</strong>
  <span>Confirm that WoWidget is open, your internet connection is working, Discord is running, and the character shown in WoWidget is the one you intend to update. Many temporary failures are resolved by closing and reopening WoWidget once.</span>
</div>

<section class="support-section" id="installation" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 1</p>
      <h2>Installation</h2>
    </div>
    <span>Windows, installer, and startup issues</span>
  </div>

  <div class="support-accordion">
    <details class="support-item" data-support-item data-search="windows protected your pc smartscreen unknown publisher run anyway installer blocked">
      <summary>
        <span class="support-item__icon">!</span>
        <span><strong>Windows says “Windows protected your PC”</strong><small>Microsoft Defender SmartScreen blocks the installer.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Why this happens</h3>
          <p>WoWidget is currently distributed without a commercial code-signing certificate. SmartScreen often warns about unsigned applications until they have established reputation.</p>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Confirm that the installer came from the official WoWidget GitHub Releases page.</li>
            <li>Select <strong>More info</strong> in the SmartScreen window.</li>
            <li>Select <strong>Run anyway</strong>.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="installer does not open launch start corrupted incomplete download antivirus quarantine defender">
      <summary>
        <span class="support-item__icon">↓</span>
        <span><strong>The installer does not open</strong><small>Nothing happens after double-clicking the downloaded installer.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Likely causes</h3>
          <ul>
            <li>The download was incomplete or corrupted.</li>
            <li>Windows Security or another antivirus product quarantined the file.</li>
            <li>A previous installer process is still running in the background.</li>
          </ul>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Delete the downloaded installer and download a fresh copy from GitHub Releases.</li>
            <li>Open <strong>Windows Security → Virus &amp; threat protection → Protection history</strong> and check whether the installer was blocked.</li>
            <li>Restart Windows, then run the installer again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="wowidget opens then disappears no window tray minimized taskbar system tray already running">
      <summary>
        <span class="support-item__icon">▣</span>
        <span><strong>WoWidget appears to open, then disappears</strong><small>The application may already be running in the system tray.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Why this happens</h3>
          <p>If <strong>Start application minimized</strong> is enabled, WoWidget can launch directly into the Windows notification area instead of opening a full window.</p>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Select the <strong>Show hidden icons</strong> arrow near the Windows clock.</li>
            <li>Locate the WoWidget icon and open it.</li>
            <li>To change this behavior, open <strong>Settings</strong> and disable <strong>Start application minimized</strong>.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="reinstall update newer version old version repair uninstall install files missing">
      <summary>
        <span class="support-item__icon">↻</span>
        <span><strong>WoWidget behaves incorrectly after an update</strong><small>A previous installation may not have been replaced cleanly.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close WoWidget completely, including its system-tray process.</li>
            <li>Run the newest installer again and allow it to replace the existing version.</li>
            <li>Restart WoWidget and test the same action once more.</li>
          </ol>
          <p>Your stored credentials are kept separately in Windows Credential Manager and normally do not need to be entered again.</p>
        </div>
      </div>
    </details>
  </div>
</section>

<section class="support-section" id="blizzard" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 2</p>
      <h2>Blizzard</h2>
    </div>
    <span>Developer credentials and character-data issues</span>
  </div>

  <div class="support-accordion">
    <details class="support-item" data-support-item data-search="credential validation failed blizzard client id client secret invalid unauthorized 401">
      <summary>
        <span class="support-item__icon">B</span>
        <span><strong>“Credential validation failed” for Blizzard</strong><small>The Client ID or Client Secret could not be authenticated.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Common causes</h3>
          <ul>
            <li>The Client ID and Client Secret were pasted into the opposite fields.</li>
            <li>A leading or trailing space was copied with one of the values.</li>
            <li>The Blizzard client was deleted or regenerated after the values were copied.</li>
          </ul>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Return to your Blizzard Developer Portal client.</li>
            <li>Copy the <strong>Client ID</strong> and <strong>Client Secret</strong> again.</li>
            <li>Paste each value into its matching WoWidget field without editing it.</li>
            <li>Select <strong>Validate and Continue</strong> once.</li>
          </ol>
          <p><a href="../getting-started/blizzard-setup/">Review the Blizzard Setup guide →</a></p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="character lookup failed character not found realm region spelling search no result 404">
      <summary>
        <span class="support-item__icon">?</span>
        <span><strong>“Character lookup failed” or character not found</strong><small>Blizzard could not match the region, realm, and character combination.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Confirm the correct region is selected.</li>
            <li>Enter the realm’s displayed name without extra punctuation or spaces.</li>
            <li>Confirm the character name is spelled correctly.</li>
            <li>Log into the character in World of Warcraft once, log out normally, wait a few minutes, and search again.</li>
          </ol>
        </div>
        <div class="support-answer">
          <h3>Still not found?</h3>
          <p>Recently transferred, renamed, restored, or newly created characters can take time to appear through Blizzard’s profile API.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="unable to contact blizzard timeout api unavailable network service outage rate limit connection">
      <summary>
        <span class="support-item__icon">⌁</span>
        <span><strong>“Unable to contact Blizzard”</strong><small>The Blizzard API request timed out or returned a temporary service error.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Confirm that your internet connection is working.</li>
            <li>Wait several minutes and try again.</li>
            <li>Check whether a VPN, firewall, DNS filter, or antivirus web shield is blocking WoWidget.</li>
            <li>If other Blizzard services are also unavailable, wait for service to recover.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="stats data old stale not updated item level mythic raid progression achievement last login cache">
      <summary>
        <span class="support-item__icon">↺</span>
        <span><strong>Character data looks old or incomplete</strong><small>Item level, Mythic+, raid progress, or collections have not caught up yet.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Why this happens</h3>
          <p>WoWidget displays data returned by Blizzard. Some profile information is cached and does not update immediately after every in-game change.</p>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Log out of the character normally so Blizzard can update the profile.</li>
            <li>Wait several minutes.</li>
            <li>Select <strong>Update Widget Now</strong> again.</li>
          </ol>
        </div>
      </div>
    </details>
  </div>
</section>

<section class="support-section" id="discord" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 3</p>
      <h2>Discord</h2>
    </div>
    <span>OAuth, Social SDK, tokens, and authorization</span>
  </div>

  <div class="support-accordion">
    <details class="support-item support-item--important" data-support-item data-search="discord authorization cancelled invalid unknown malformed scope social sdk form required">
      <summary>
        <span class="support-item__icon">!</span>
        <span><strong>“Discord Authorization Cancelled” or “scope is invalid, unknown or malformed”</strong><small>The Discord Social SDK setup form has not been completed.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open your application in the Discord Developer Portal.</li>
            <li>Open <strong>Social SDK</strong> under the Games section.</li>
            <li>Complete every required field, accept the privacy-policy acknowledgement, and submit the form.</li>
            <li>Return to WoWidget and select <strong>Authorize Discord</strong> again.</li>
          </ol>
          <p><a href="../getting-started/discord-setup/">Go to Discord Setup: Social SDK Form →</a></p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="redirect uri mismatch oauth invalid redirect callback 127.0.0.1 5001 discord">
      <summary>
        <span class="support-item__icon">↪</span>
        <span><strong>Discord reports an invalid or mismatched redirect URI</strong><small>The OAuth redirect in the Developer Portal does not exactly match WoWidget.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open <strong>OAuth2</strong> in your Discord application.</li>
            <li>Add the following redirect exactly as written:</li>
          </ol>
          <div class="copy-field">
            <code>http://127.0.0.1:5001/callback</code>
            <button class="copy-button" type="button" data-copy="http://127.0.0.1:5001/callback">Copy</button>
          </div>
          <ol start="3">
            <li>Select <strong>Save Changes</strong>.</li>
            <li>Try authorization again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="could not start authorization callback port 5001 in use address already used oauth">
      <summary>
        <span class="support-item__icon">5001</span>
        <span><strong>“Could not start the Discord authorization callback on port 5001”</strong><small>Another program is already using WoWidget’s local callback port.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close any other WoWidget window or background instance.</li>
            <li>Close local development servers or other applications using port 5001.</li>
            <li>Restart WoWidget and authorize again.</li>
            <li>If necessary, restart Windows to release the port.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="discord authorization timed out browser accept no callback timeout authorize again">
      <summary>
        <span class="support-item__icon">⌛</span>
        <span><strong>“Discord authorization timed out”</strong><small>The browser authorization was not completed before WoWidget stopped waiting.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close the old Discord authorization tab.</li>
            <li>Select <strong>Authorize Discord</strong> again.</li>
            <li>Complete the browser prompt without refreshing or opening a second authorization attempt.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="invalid oauth state authorization cancelled for safety multiple tabs state error discord">
      <summary>
        <span class="support-item__icon">⌁</span>
        <span><strong>“Discord returned an invalid OAuth state”</strong><small>The callback did not match the authorization attempt WoWidget started.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close all open Discord authorization tabs.</li>
            <li>Restart WoWidget.</li>
            <li>Start one new authorization attempt and complete only that tab.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="wrong discord account authorized account switch logout browser incognito profile">
      <summary>
        <span class="support-item__icon">@</span>
        <span><strong>The wrong Discord account was authorized</strong><small>Your browser was already signed into another Discord account.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open WoWidget <strong>Settings</strong>.</li>
            <li>Authorize Discord again.</li>
            <li>In the browser, sign out of the incorrect Discord account or use a private window with the intended account.</li>
            <li>Confirm the displayed account name before accepting.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="discord token refresh failed access token expired authorize again settings disconnected">
      <summary>
        <span class="support-item__icon">↻</span>
        <span><strong>“Discord token refresh failed” or Discord becomes unauthorized</strong><small>The saved OAuth session expired or was revoked.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open WoWidget <strong>Settings</strong>.</li>
            <li>Select <strong>Authorize Discord</strong>.</li>
            <li>Accept the browser authorization request again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="bot token invalid missing discord token credential validation failed reset token regenerate">
      <summary>
        <span class="support-item__icon">#</span>
        <span><strong>The Discord Bot Token is rejected</strong><small>The token is missing, incomplete, reset, or copied from the wrong field.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open <strong>Bot</strong> in the Discord Developer Portal.</li>
            <li>Select <strong>Reset Token</strong> only if you no longer have the current token.</li>
            <li>Copy the full Bot Token and paste it into WoWidget.</li>
            <li>Do not use the Public Key, Application ID, or Client Secret in the Bot Token field.</li>
          </ol>
        </div>
      </div>
    </details>
  </div>
</section>

<section class="support-section" id="widget-editor" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 4</p>
      <h2>Widget Editor</h2>
    </div>
    <span>Experimental editor, publishing, and variables</span>
  </div>

  <div class="support-accordion">
    <details class="support-item" data-support-item data-search="widget tab missing experimental widget editor developer console enable not visible">
      <summary>
        <span class="support-item__icon">W</span>
        <span><strong>The Widget tab is missing</strong><small>The experimental Widget Editor has not been enabled for the current portal session.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Return to the Discord Developer Portal home screen using the portal’s back arrow.</li>
            <li>Repeat the experimental Widget Editor enablement step in your browser console.</li>
            <li>Close Developer Tools and reopen your Discord application.</li>
          </ol>
          <p><a href="../../getting-started/discord-setup/">Review Discord Setup: Experimental Widget Editor →</a></p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="widget editor disappeared after refresh page reload experimental access repeat console">
      <summary>
        <span class="support-item__icon">↺</span>
        <span><strong>The Widget tab disappeared after refreshing the page</strong><small>Experimental access is temporary and tied to the current portal session.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <p>Repeat the Widget Editor enablement step. Avoid refreshing the Developer Portal until the widget has been saved and published.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="publish button missing cannot publish widget preview add widget preview required">
      <summary>
        <span class="support-item__icon">↑</span>
        <span><strong>The widget cannot be published or added to the profile</strong><small>The required Widget Preview may be missing.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Use the Widget Editor dropdown and select <strong>Add Widget Preview</strong>.</li>
            <li>Choose the Hero layout.</li>
            <li>Configure its image with the required <code>character_model</code> User Data field.</li>
            <li>Select <strong>Save changes</strong>, then <strong>Publish</strong>.</li>
          </ol>
          <p><a href="../../getting-started/widget-editor/">Review Widget Setup: Widget Preview →</a></p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="widget field blank not updating variable typo data field value type fallback exact configuration">
      <summary>
        <span class="support-item__icon">_</span>
        <span><strong>A widget field is blank or never updates</strong><small>The Data Field, Value Type, Presentation Type, or fallback does not match WoWidget.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Most common cause</h3>
          <p>User Data variable names are exact and case-sensitive. Even a small spelling difference creates a different variable.</p>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Compare the field against the Widget Setup guide.</li>
            <li>Confirm the exact <strong>Data Field</strong> name.</li>
            <li>Confirm the required <strong>Value Type</strong> and <strong>Presentation Type</strong>.</li>
            <li>Save and publish the widget again.</li>
            <li>Return to WoWidget and select <strong>Update Widget Now</strong>.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="character image portrait missing character_model image user data widget top preview">
      <summary>
        <span class="support-item__icon">▧</span>
        <span><strong>The character image does not appear</strong><small>The image element or preview is using the wrong Data Field.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Required configuration</h3>
          <ul>
            <li><strong>Value Type:</strong> User Data</li>
            <li><strong>Data Field:</strong> <code>character_model</code></li>
            <li><strong>Fallback:</strong> Disabled</li>
          </ul>
          <p>Use the same image field in both <strong>Widget Top</strong> and <strong>Widget Preview</strong>.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="faction icon spec icon missing wrong icon user data field faction_icon spec_icon">
      <summary>
        <span class="support-item__icon">◇</span>
        <span><strong>The faction or specialization icon is missing</strong><small>The icon control is disabled or points to the wrong User Data field.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ul>
            <li>For Widget Top Subtitle 1, enable the icon and use <code>faction_icon</code>.</li>
            <li>For the Current Spec stat, enable the icon and use <code>spec_icon</code>.</li>
            <li>Set the icon Value Type to <strong>User Data</strong>.</li>
          </ul>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="stat unavailable n/a pvp raid no data expected unsupported no rating">
      <summary>
        <span class="support-item__icon">N/A</span>
        <span><strong>A statistic displays “Unavailable” or “N/A”</strong><small>WoWidget may not have usable data for that character and statistic.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Examples</h3>
          <ul>
            <li>A character with no current PvP rating.</li>
            <li>A character with no progression in the tracked raid tier.</li>
            <li>A Blizzard profile endpoint that does not expose the requested value.</li>
          </ul>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <p>Choose a different statistic for that slot, or configure an appropriate fallback in the Widget Editor where supported.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="last logged in last_login duration incorrect huge number milliseconds presentation type duration">
      <summary>
        <span class="support-item__icon">◷</span>
        <span><strong>Last Logged In displays an incorrect number</strong><small>The field is not configured with Discord’s Duration presentation.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Required configuration</h3>
          <ul>
            <li><strong>Presentation Type:</strong> Duration</li>
            <li><strong>Data Field:</strong> <code>last_login</code></li>
          </ul>
          <p>Do not configure <code>last_login</code> as plain Text or Number.</p>
        </div>
      </div>
    </details>
  </div>
</section>

<section class="support-section" id="application" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 5</p>
      <h2>WoWidget Application</h2>
    </div>
    <span>Updates, portraits, background service, and settings</span>
  </div>

  <div class="support-accordion">
    <details class="support-item" data-support-item data-search="unable to save setup information credential windows credential manager keyring save load error">
      <summary>
        <span class="support-item__icon">🔒</span>
        <span><strong>“Unable to save setup information” or “Unable to save credential”</strong><small>Windows Credential Manager could not store one of WoWidget’s secrets.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close WoWidget and restart Windows.</li>
            <li>Open WoWidget normally and retry validation.</li>
            <li>Confirm that Windows Credential Manager is available and that security software is not blocking credential storage.</li>
            <li>If the error continues, open <strong>Credential Manager → Windows Credentials</strong>, remove stale entries named <strong>WoWidget</strong>, then repeat setup.</li>
          </ol>
          <p class="support-note"><strong>Note:</strong> Removing WoWidget credentials requires you to enter and authorize them again.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="update widget now failed error not updating discord push manual update last error">
      <summary>
        <span class="support-item__icon">↥</span>
        <span><strong>“Update Widget Now” fails</strong><small>The most recent error may come from Blizzard, Discord, image upload, or authorization.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Read the exact <strong>Last Error</strong> shown on the WoWidget dashboard.</li>
            <li>If Discord is unauthorized, open Settings and authorize it again.</li>
            <li>If Blizzard cannot be contacted, wait briefly and retry.</li>
            <li>If the portrait upload fails, use <strong>Repair Upload Registration</strong> in Settings, then update again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="repair upload registration cloudflare registration installation token image uploader no token service returned">
      <summary>
        <span class="support-item__icon">☁</span>
        <span><strong>Portrait upload or upload registration fails</strong><small>WoWidget’s installation token may be missing or no longer valid.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open WoWidget <strong>Settings</strong>.</li>
            <li>Select <strong>Repair Upload Registration</strong>.</li>
            <li>Wait for the success message.</li>
            <li>Select <strong>Update Widget Now</strong> again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="browser does not open authorize discord default browser blocked webbrowser popup">
      <summary>
        <span class="support-item__icon">↗</span>
        <span><strong>The browser does not open when authorizing Discord</strong><small>Windows could not open the authorization URL with the default browser.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Confirm that Windows has a default web browser configured.</li>
            <li>Close and reopen WoWidget.</li>
            <li>Temporarily disable browser pop-up restrictions or security software that intercepts links.</li>
            <li>Select <strong>Authorize Discord</strong> again.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="portrait generate fails blank render character model raw file rendering unavailable">
      <summary>
        <span class="support-item__icon">✦</span>
        <span><strong>The portrait does not generate</strong><small>The character render could not be downloaded or processed.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Confirm the selected character is correct.</li>
            <li>Check your internet connection.</li>
            <li>Wait a few minutes and select <strong>Generate Portrait</strong> again.</li>
            <li>If Blizzard does not provide a usable render for the character, try again after logging into that character and logging out normally.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="portrait cropped cut off too small position top right fade save portrait editor zoom drag">
      <summary>
        <span class="support-item__icon">⌖</span>
        <span><strong>The portrait is cropped or positioned poorly</strong><small>The saved crop does not account for the widget’s fade and visible area.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open the Portrait Editor.</li>
            <li>Move the character toward the <strong>top-right</strong> of the visible crop area.</li>
            <li>Keep important details away from the left-side fade region.</li>
            <li>Select <strong>Save Portrait</strong>, then update the widget and review the result.</li>
            <li>Repeat as needed; saving another crop does not require regenerating the raw render.</li>
          </ol>
          <p><a href="../using-wowidget/portrait-studio/">Open the Portrait Studio guide →</a></p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="automatic updates not running auto update interval app closed minimized background timer enable">
      <summary>
        <span class="support-item__icon">⟳</span>
        <span><strong>Automatic updates are not running</strong><small>WoWidget must remain open and automatic updates must be enabled.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open <strong>Settings</strong> and confirm automatic updates are enabled.</li>
            <li>Confirm the update interval is set to the value you expect.</li>
            <li>Keep WoWidget running; minimizing it is fine, but fully exiting stops the timer.</li>
            <li>Check the dashboard for the last update time and any displayed error.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="launch with windows startup does not work registry disabled startup apps setting start minimized">
      <summary>
        <span class="support-item__icon">⊞</span>
        <span><strong>Launch with Windows does not work</strong><small>The startup entry could not be created or has been disabled by Windows.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Open WoWidget <strong>Settings</strong>.</li>
            <li>Disable <strong>Launch with Windows</strong>, save, then enable it again and save.</li>
            <li>Open <strong>Windows Settings → Apps → Startup</strong> and confirm WoWidget is permitted.</li>
            <li>If a security utility manages startup items, allow WoWidget there as well.</li>
          </ol>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="widget did not change after publish update data stale save changes publish update widget now">
      <summary>
        <span class="support-item__icon">✓</span>
        <span><strong>Widget Editor changes do not appear on the profile</strong><small>Publishing the layout and pushing new User Data are separate actions.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>In the Discord Widget Editor, select <strong>Save changes</strong>.</li>
            <li>Select <strong>Publish</strong>.</li>
            <li>Return to WoWidget and select <strong>Update Widget Now</strong>.</li>
            <li>Reopen or refresh your Discord profile after the update completes.</li>
          </ol>
        </div>
      </div>
    </details>
  </div>
</section>

<section class="support-section" id="advanced" data-support-section>
  <div class="support-section__heading">
    <div>
      <p>Category 6</p>
      <h2>Advanced Recovery</h2>
    </div>
    <span>Use these only after the targeted fix above has failed</span>
  </div>

  <div class="support-accordion">
    <details class="support-item" data-support-item data-search="where app data logs generated files localappdata folder open application data diagnostics">
      <summary>
        <span class="support-item__icon">…</span>
        <span><strong>Open WoWidget’s application-data folder</strong><small>Useful when collecting diagnostic information or reviewing generated portraits.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Recommended method</h3>
          <p>Open WoWidget <strong>Settings</strong> and use the built-in button to open the application-data folder. This avoids manually navigating to hidden Windows directories.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="reset discord authorization credentials clear reauthorize credential manager windows credentials wowidget">
      <summary>
        <span class="support-item__icon">↺</span>
        <span><strong>Reset saved Discord authorization</strong><small>Use when repeated reauthorization attempts continue to use broken or stale credentials.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Close WoWidget.</li>
            <li>Open <strong>Control Panel → Credential Manager → Windows Credentials</strong>.</li>
            <li>Remove WoWidget entries related to Discord authorization.</li>
            <li>Reopen WoWidget and complete Discord authorization again.</li>
          </ol>
          <p class="support-note"><strong>Use caution:</strong> Removing all WoWidget entries also removes Blizzard and Discord setup credentials, requiring complete setup again.</p>
        </div>
      </div>
    </details>

    <details class="support-item" data-support-item data-search="clean reset factory reset reinstall remove settings credentials start over complete setup">
      <summary>
        <span class="support-item__icon">×</span>
        <span><strong>Perform a complete WoWidget reset</strong><small>Last-resort recovery when the installation and saved configuration are both unusable.</small></span>
      </summary>
      <div class="support-item__body">
        <div class="support-answer">
          <h3>Before continuing</h3>
          <p>This removes your saved setup and requires you to repeat Blizzard, Discord, Widget, and Application setup.</p>
        </div>
        <div class="support-answer support-answer--solution">
          <h3>Resolution</h3>
          <ol>
            <li>Save copies of your Blizzard and Discord developer credentials.</li>
            <li>Close and uninstall WoWidget.</li>
            <li>Remove WoWidget entries from Windows Credential Manager.</li>
            <li>Remove the WoWidget application-data folder using the location opened from Settings before uninstalling, if available.</li>
            <li>Install the newest release and repeat the setup guides from the beginning.</li>
          </ol>
        </div>
      </div>
    </details>
  </div>
</section>

<div id="troubleshooting-empty" class="support-empty" hidden>
  <span>?</span>
  <h2>No matching issue found</h2>
  <p>Try a shorter search such as <strong>authorization</strong>, <strong>portrait</strong>, <strong>character</strong>, or part of the exact error message.</p>
</div>

<section class="support-report">
  <div>
    <p class="support-report__eyebrow">Still stuck?</p>
    <h2>Report an issue with useful details</h2>
    <p>Include the exact error text, the action that triggered it, your WoWidget version, and a screenshot with all secrets hidden.</p>
  </div>
  <div class="support-report__checklist">
    <span>✓ Exact error message</span>
    <span>✓ WoWidget version</span>
    <span>✓ Steps to reproduce</span>
    <span>✓ Redacted screenshot</span>
  </div>
  <a class="md-button md-button--primary" href="https://github.com/solxvt/WoWidget/issues">Open a GitHub Issue</a>
</section>
