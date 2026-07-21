---
hide:
  - toc
  - navigation
---

<div class="guide-hero usage-hero">
  <p class="guide-hero__eyebrow">Using WoWidget</p>
  <h1>Updating Your Widget</h1>
  <p class="guide-hero__summary">Send an immediate refresh, configure automatic updates, and understand when new World of Warcraft data appears on your Discord profile.</p>
  <div class="guide-meta"><span>Manual or scheduled</span><span>WoWidget must be running</span></div>
</div>

<div class="usage-overview">
  <a href="#manual-updates"><span>01</span><strong>Update now</strong><small>Send an immediate refresh.</small></a>
  <a href="#automatic-updates"><span>02</span><strong>Automate</strong><small>Choose a background interval.</small></a>
  <a href="#what-gets-updated"><span>03</span><strong>Understand</strong><small>Know what data is refreshed.</small></a>
</div>

<section class="guide-step guide-step--split" id="manual-updates">
  <div class="guide-step__copy">
    <div class="guide-step__heading"><span class="step-number">1</span><h2>Run a manual update</h2></div>
    <p>Select <strong>Update Widget Now</strong> whenever you want WoWidget to request current character information and send a fresh payload to Discord.</p>
    <p>A manual update is useful after changing characters, saving a new portrait, reaching a progression milestone, or adjusting the variables configured in Discord's Widget Editor.</p>
    <aside class="ww-callout ww-callout--tip"><strong>Save the portrait first</strong><span>The update uses the most recently saved portrait. Unsaved positioning changes in Portrait Studio are not sent to Discord.</span></aside>
  </div>
  <figure class="doc-screenshot">
    <img src="../../assets/images/application/07-update-widget.png" alt="WoWidget Update Widget Now control" loading="lazy">
    <figcaption>Use Update Widget Now for an immediate refresh.</figcaption>
  </figure>
</section>

<section class="guide-step guide-step--split" id="automatic-updates">
  <div class="guide-step__copy">
    <div class="guide-step__heading"><span class="step-number">2</span><h2>Configure automatic updates</h2></div>
    <p>Open <strong>Settings</strong>, enable automatic updates, and choose the interval that fits how often you play. WoWidget remains idle between checks and updates only while the application is running.</p>

    <div class="interval-guide">
      <div><strong>30 minutes</strong><span>Best for active sessions and frequent progression changes.</span></div>
      <div><strong>1 hour</strong><span>Recommended balance for most users.</span></div>
      <div><strong>Longer intervals</strong><span>Appropriate when the widget changes infrequently.</span></div>
    </div>
  </div>
  <figure class="doc-screenshot">
    <img src="../../assets/images/application/08-settings-features.png" alt="WoWidget settings with startup and update options" loading="lazy">
    <figcaption>Choose startup behavior and an automatic update interval.</figcaption>
  </figure>
</section>

<aside class="ww-callout ww-callout--note"><strong>Background updates require a running application</strong><span>Closing WoWidget stops scheduled checks. Enable <strong>Launch at Windows startup</strong> and <strong>Start application minimized</strong> for hands-off updates.</span></aside>

<section class="guide-step" id="what-gets-updated">
  <div class="guide-step__heading"><span class="step-number">3</span><h2>What gets updated</h2></div>
  <p>Each update rebuilds the values used by the published Discord widget. The exact statistics visible on your profile depend on the fields you selected in the Widget Editor.</p>

  <div class="update-data-grid">
    <article><span>Identity</span><strong>Name, realm, race, class, specialization, guild, faction</strong></article>
    <article><span>Progression</span><strong>Item level, Mythic+, PvP, and current-season raid progress</strong></article>
    <article><span>Collections</span><strong>Achievements, mounts, pets, titles, reputations, and related totals</strong></article>
    <article><span>Images</span><strong>Saved character portrait, specialization icon, and faction icon</strong></article>
  </div>

  <aside class="ww-callout ww-callout--note"><strong>Source data can lag behind the game</strong><span>WoWidget can only send the information currently returned by Blizzard. Logging out, changing equipment, or earning progress does not guarantee that Blizzard's profile data updates immediately.</span></aside>
</section>

<section class="guide-step" id="confirm-the-update">
  <div class="guide-step__heading"><span class="step-number">4</span><h2>Confirm the result</h2></div>
  <div class="usage-action-grid">
    <article>
      <span>WoWidget</span>
      <h3>Check the update status</h3>
      <p>Confirm that the application reports a successful refresh rather than a validation, Blizzard, or Discord error.</p>
    </article>
    <article>
      <span>Discord</span>
      <h3>Open your profile</h3>
      <p>View the Board tab and inspect the published widget. Discord may take a short time to display the newest values.</p>
    </article>
    <article>
      <span>Still stale?</span>
      <h3>Run the quick checks</h3>
      <p>Restart WoWidget, confirm the selected character, and review the Troubleshooting guide for stale-data or authorization issues.</p>
    </article>
  </div>
</section>

<div class="guide-panel usage-next">
  <div>
    <p class="guide-hero__eyebrow">Reference</p>
    <h2>Browse every widget field</h2>
    <p>Use the variable reference when configuring or changing the statistics displayed by Discord.</p>
  </div>
  <a class="md-button md-button--primary" href="../../reference/widget-variables/">Open Widget Variables</a>
</div>
