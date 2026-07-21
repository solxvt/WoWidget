---
hide:
  - toc
  - navigation
---

<div class="guide-hero">
  <p class="guide-hero__eyebrow">Getting Started · Step 2 of 5</p>
  <h1>Blizzard Setup</h1>
  <p class="guide-hero__summary">Create a personal Blizzard API client so WoWidget can retrieve your public World of Warcraft character data.</p>
  <div class="guide-meta"><span>⏱ 3–5 minutes</span><span>Battle.net account required</span><span>Read-only character data</span></div>
</div>

<nav class="setup-progress" aria-label="Setup progress">
  <ol>
    <li class="is-complete"><a href="../installation/" data-step="1"><span class="setup-progress__marker" data-step="1" aria-hidden="true"></span><span class="setup-progress__label">Installation</span></a></li>
    <li class="is-current" aria-current="step"><a href="../blizzard-setup/" data-step="2"><span class="setup-progress__marker" data-step="2" aria-hidden="true"></span><span class="setup-progress__label">Blizzard</span></a></li>
    <li><a href="../discord-setup/" data-step="3"><span class="setup-progress__marker" data-step="3" aria-hidden="true"></span><span class="setup-progress__label">Discord</span></a></li>
    <li><a href="../widget-editor/" data-step="4"><span class="setup-progress__marker" data-step="4" aria-hidden="true"></span><span class="setup-progress__label">Widget</span></a></li>
    <li><a href="../application-setup/" data-step="5"><span class="setup-progress__marker" data-step="5" aria-hidden="true"></span><span class="setup-progress__label">Application</span></a></li>
  </ol>
</nav>

<div class="guide-panel" markdown="1">
<h2>Before you begin</h2>
<p>Open the <a href="https://develop.battle.net/">Blizzard Developer Portal</a> and sign in with your Battle.net account. Your API client is personal and should not be shared.</p>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">1</span><h2>Open Blizzard Setup</h2></div>
<p>After signing in, select <strong>Get Started Now</strong>.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/blizzard/01-get-started.png" alt="Blizzard Developer Portal with Get Started Now highlighted" loading="lazy">
  <figcaption>Sign in, then select Get Started Now.</figcaption>
</figure>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">2</span><h2>Create a client</h2></div>
<p>Select <strong>Create Client</strong>.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/blizzard/02-create-client.png" alt="Blizzard Developer Portal Create Client button" loading="lazy">
  <figcaption>Create a personal API client for WoWidget.</figcaption>
</figure>
</div>

!!! note "Keep the client private"
    Blizzard developer clients are personal and unique. Do not share the client or its credentials with anyone.

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">3</span><h2>Configure the client</h2></div>
<p>Enter a unique client name. Copy the URL shown below into both <strong>Redirect URLs</strong> and <strong>Service URL</strong>, add a short description, and select <strong>Save</strong>.</p>
<div class="copy-field"><code>http://localhost</code><button class="copy-button" data-copy="http://localhost">Copy</button></div>
<p>The client name can be anything unique. It is not displayed on your Discord widget.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/blizzard/03-client-setup.png" alt="Blizzard client setup form" loading="lazy">
  <figcaption>Enter the client name, URLs, and description exactly as shown.</figcaption>
</figure>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">4</span><h2>Save your API credentials</h2></div>
<p>Copy the <strong>Client ID</strong> and <strong>Client Secret</strong> into a temporary text file and label each value. You will enter both into WoWidget later.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/blizzard/04-api-tokens.png" alt="Blizzard API Client ID and Client Secret" loading="lazy">
  <figcaption>Copy and label both API credentials for later use.</figcaption>
</figure>
</div>

!!! danger "Never share your Client Secret"
    Treat the Client Secret like a password. Do not include it in screenshots, support posts, or GitHub commits. WoWidget stores saved credentials in Windows Credential Manager.

