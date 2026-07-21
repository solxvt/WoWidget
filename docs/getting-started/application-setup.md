---
hide:
  - toc
  - navigation
---

<div class="guide-hero">
  <p class="guide-hero__eyebrow">Getting Started · Step 5 of 5</p>
  <h1>Application Setup</h1>
  <p class="guide-hero__summary">Connect your credentials, authorize Discord, select a character, create a portrait, and send your first live widget update.</p>
  <div class="guide-meta"><span>⏱ 5–10 minutes</span><span>WoWidget installed</span></div>
</div>

<nav class="setup-progress" aria-label="Setup progress">
  <ol>
    <li class="is-complete"><a href="../installation/" data-step="1"><span class="setup-progress__marker" data-step="1" aria-hidden="true"></span><span class="setup-progress__label">Installation</span></a></li>
    <li class="is-complete"><a href="../blizzard-setup/" data-step="2"><span class="setup-progress__marker" data-step="2" aria-hidden="true"></span><span class="setup-progress__label">Blizzard</span></a></li>
    <li class="is-complete"><a href="../discord-setup/" data-step="3"><span class="setup-progress__marker" data-step="3" aria-hidden="true"></span><span class="setup-progress__label">Discord</span></a></li>
    <li class="is-complete"><a href="../widget-editor/" data-step="4"><span class="setup-progress__marker" data-step="4" aria-hidden="true"></span><span class="setup-progress__label">Widget</span></a></li>
    <li class="is-current" aria-current="step"><a href="../application-setup/" data-step="5"><span class="setup-progress__marker" data-step="5" aria-hidden="true"></span><span class="setup-progress__label">Application</span></a></li>
  </ol>
</nav>

<div class="guide-panel" markdown="1">
<h2>Before you begin</h2>
<p>Have your Blizzard Client ID and Client Secret, Discord Application ID, Discord Client Secret, and Discord Bot Token ready. Download the latest build from <a href="https://github.com/solxvt/WoWidget/releases/latest">GitHub Releases</a> if WoWidget is not already installed.</p>
</div>

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">1</span><h2>Enter your credentials</h2></div>
<p>Paste each credential into the matching WoWidget field, then select <strong>Validate and Continue</strong> once.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/01-input-credentials.png" alt="WoWidget credential setup screen" loading="lazy">
  <figcaption>Paste each saved credential into its matching field.</figcaption>
</figure>
</div>

<div class="guide-step" markdown="1">
<div class="guide-step__heading"><span class="step-number">2</span><h2>Authorize Discord</h2></div>
<p>When <strong>Authorize your Discord</strong> appears, select it. Your browser will open an authorization request for the Discord application you created. Approve the request, then return to WoWidget.</p>
<div class="screenshot-gallery screenshot-gallery--3">
<figure class="doc-screenshot">
  <img src="../../assets/images/application/02-authorize-button.png" alt="WoWidget Authorize your Discord button" loading="lazy">
  <figcaption>Start the one-time Discord authorization from WoWidget.</figcaption>
</figure>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/03-discord-authorization.png" alt="Discord OAuth authorization screen" loading="lazy">
  <figcaption>Review and approve the authorization request for your application.</figcaption>
</figure>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/04-authorization-success.png" alt="WoWidget Discord authorization success state" loading="lazy">
  <figcaption>Return to WoWidget after authorization succeeds.</figcaption>
</figure>
</div>
</div>

!!! question "Why does Discord request several permissions?"
    Discord currently groups Social SDK functionality into one authorization scope. WoWidget uses the Widget-related functionality, but Discord may display the broader Social SDK permission set. Because you created and own the application, you are authorizing your own Discord application.

!!! warning "Authorization cancelled"
    If you see **Discord Authorization Cancelled** or an invalid-scope error, complete [Discord Setup, Step 5](../discord-setup/#complete-the-social-sdk-form) and try again.

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">3</span><h2>Select your character</h2></div>
<p>Search for the character you want to display. Verify the name, realm, class, and other returned information, then select <strong>Use this Character</strong>.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/05-character-selection.png" alt="WoWidget character search and selection screen" loading="lazy">
  <figcaption>Verify the returned character, then select Use this Character.</figcaption>
</figure>
</div>

!!! note "Use characters responsibly"
    Display a character you own or have permission to use. Avoid impersonating other players.

<div class="guide-step" markdown="1">
<div class="guide-step__heading"><span class="step-number">4</span><h2>Create the portrait and update the widget</h2></div>
<p>In Portrait Editor, select <strong>Generate Portrait</strong>. Reposition the character inside the crop area, select <strong>Save Portrait</strong>, then select <strong>Update Widget Now</strong>.</p>
<div class="screenshot-gallery screenshot-gallery--2">
<figure class="doc-screenshot">
  <img src="../../assets/images/application/06-portrait-editor.png" alt="WoWidget Portrait Editor" loading="lazy">
  <figcaption>Generate, position, and save the character portrait.</figcaption>
</figure>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/07-update-widget.png" alt="WoWidget Update Widget Now control" loading="lazy">
  <figcaption>Send the completed data and portrait to Discord.</figcaption>
</figure>
</div>
</div>

!!! tip "Portrait placement"
    Position the character near the upper-right edge of the crop box. The left side receives a fade effect, and anything outside the guide lines is cropped. You may save the portrait repeatedly until it looks right. The raw render only needs to be generated once per character because it is stored locally.

<div class="guide-step guide-step--split" markdown="1">
<div class="guide-step__copy">
<div class="guide-step__heading"><span class="step-number">5</span><h2>Configure background updates</h2></div>
<p>Open <strong>Settings</strong>. For the smoothest experience, enable <strong>Launch at Windows startup</strong> and <strong>Start application minimized</strong>. You can update manually or enable automatic updates and choose an interval.</p>
<p>For active play sessions, an interval between <strong>30 minutes and 1 hour</strong> is a practical balance. WoWidget remains idle between scheduled checks and is designed to run unobtrusively in the background.</p>
</div>
<figure class="doc-screenshot">
  <img src="../../assets/images/application/08-settings-features.png" alt="WoWidget Settings page" loading="lazy">
  <figcaption>Choose startup behavior and an automatic update interval.</figcaption>
</figure>
</div>

<div class="guide-panel" markdown="1">
<h2>🎉 Setup complete</h2>
<p>Your Discord profile now has a dynamically updating World of Warcraft widget. WoWidget can refresh it manually or automatically while the application runs.</p>
<p><a class="md-button md-button--primary" href="../../using-wowidget/updating-widget/">Learn about updates</a> <a class="md-button" href="../../support/troubleshooting/">Troubleshooting</a></p>
</div>

