---
hide:
  - toc
  - navigation
---

<div class="guide-hero reference-hero">
  <p class="guide-hero__eyebrow">Reference</p>
  <h1>Widget Variables</h1>
  <p class="guide-hero__summary">A complete reference for the user-data fields used by WoWidget and Discord's Widget Editor.</p>
  <div class="guide-meta"><span>Text, number, duration, and image fields</span><span>Names are case-sensitive</span></div>
</div>

<div class="variable-reference-intro">
  <div>
    <span class="variable-reference-intro__icon">{ }</span>
    <p><strong>Match every field exactly.</strong><br>Discord connects a widget element to WoWidget by its Data Field name and Presentation Type. A spelling or type mismatch prevents the value from appearing.</p>
  </div>
  <a class="md-button" href="../../getting-started/widget-editor/">Open Widget Editor guide</a>
</div>

<section class="reference-section">
  <div class="section-heading">
    <div><p class="section-heading__eyebrow">Widget Top</p><h2>Identity and hero fields</h2></div>
    <p>These fields build the main character area of the widget.</p>
  </div>

  <div class="variable-card-grid">
    <article class="variable-card variable-card--image">
      <header><code>character_model</code><span>Image</span></header>
      <h3>Character Portrait</h3>
      <p>The portrait saved in Portrait Studio and displayed in the Hero image area.</p>
      <footer>Recommended use: Widget Top image and Widget Preview</footer>
    </article>
    <article class="variable-card">
      <header><code>character_name</code><span>Text</span></header>
      <h3>Character Name</h3>
      <p>The selected character's display name.</p>
      <footer>Recommended use: Title</footer>
    </article>
    <article class="variable-card">
      <header><code>race_class</code><span>Text</span></header>
      <h3>Race and Class</h3>
      <p>A combined identity string such as “Blood Elf Demon Hunter.”</p>
      <footer>Recommended use: Subtitle 1</footer>
    </article>
    <article class="variable-card">
      <header><code>realm</code><span>Text</span></header>
      <h3>Realm</h3>
      <p>The realm associated with the active character.</p>
      <footer>Recommended label: Realm:</footer>
    </article>
    <article class="variable-card">
      <header><code>guild</code><span>Text</span></header>
      <h3>Guild Name</h3>
      <p>The character's current guild, or the application's fallback when no guild is returned.</p>
      <footer>Recommended label: Guild:</footer>
    </article>
    <article class="variable-card variable-card--image">
      <header><code>faction_icon</code><span>Image</span></header>
      <h3>Faction Icon</h3>
      <p>The Alliance or Horde icon associated with the character.</p>
      <footer>Recommended use: Race/Class subtitle icon</footer>
    </article>
  </div>
</section>

<section class="reference-section">
  <div class="section-heading">
    <div><p class="section-heading__eyebrow">Widget Bottom</p><h2>Required specialization fields</h2></div>
    <p>Use these together for the first Stats Grid slot.</p>
  </div>

  <div class="variable-card-grid variable-card-grid--compact">
    <article class="variable-card">
      <header><code>spec_name</code><span>Text</span></header>
      <h3>Current Specialization</h3>
      <p>The active specialization name used as the first stat value.</p>
      <footer>Recommended label: Current Spec</footer>
    </article>
    <article class="variable-card variable-card--image">
      <header><code>spec_icon</code><span>Image</span></header>
      <h3>Specialization Icon</h3>
      <p>The icon corresponding to the active character specialization.</p>
      <footer>Recommended use: Stat 1 icon</footer>
    </article>
  </div>
</section>

<section class="reference-section">
  <div class="section-heading">
    <div><p class="section-heading__eyebrow">Stats 2–6</p><h2>Optional statistics</h2></div>
    <p>Choose any five fields supported by your current WoWidget build.</p>
  </div>

  <div class="table-shell variable-reference-table-shell">
    <table class="variable-table variable-reference-table">
      <thead>
        <tr><th>Display name</th><th>Presentation type</th><th>Data field</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td>Item Level</td><td><span class="type-chip">Number</span></td><td><code>gear_score</code></td><td>Current equipped item level.</td></tr>
        <tr><td>Mythic+ Rating</td><td><span class="type-chip">Number</span></td><td><code>mythic_score</code></td><td>Current Mythic+ rating returned by Blizzard.</td></tr>
        <tr><td>Mythic+ Rating (Exact)</td><td><span class="type-chip type-chip--text">Text</span></td><td><code>mythic_score2</code></td><td>Exact Mythic+ rating with thousands separators, such as <code>3,428</code>.</td></tr>
        <tr><td>PvP Rating</td><td><span class="type-chip type-chip--text">Text</span></td><td><code>pvp_score</code></td><td>Current supported PvP rating.</td></tr>
        <tr><td>Raid Progress</td><td><span class="type-chip type-chip--text">Text</span></td><td><code>raid_score</code></td><td>Combined current-season raid progression.</td></tr>
        <tr><td>Achievements</td><td><span class="type-chip">Number</span></td><td><code>a_score</code></td><td>Total achievement points.</td></tr>
        <tr><td>Achievements (Exact)</td><td><span class="type-chip type-chip--text">Text</span></td><td><code>a_score2</code></td><td>Exact achievement points with thousands separators, such as <code>27,345</code>.</td></tr>
        <tr><td>Mounts</td><td><span class="type-chip">Number</span></td><td><code>mount_score</code></td><td>Number of collected mounts.</td></tr>
        <tr><td>Pets</td><td><span class="type-chip">Number</span></td><td><code>pet_score</code></td><td>Number of collected companion pets.</td></tr>
        <tr><td>Titles</td><td><span class="type-chip">Number</span></td><td><code>title_score</code></td><td>Number of unlocked character titles.</td></tr>
        <tr><td>Feats of Strength</td><td><span class="type-chip">Number</span></td><td><code>feats_score</code></td><td>Completed Feats of Strength.</td></tr>
        <tr><td>Exalted Reputations</td><td><span class="type-chip">Number</span></td><td><code>rep_score</code></td><td>Number of reputations at Exalted.</td></tr>
        <tr><td>Last Logged In</td><td><span class="type-chip type-chip--text">Text</span></td><td><code>last_login</code></td><td>Elapsed time since the character last logged in.</td></tr>
        <tr><td>Character Level</td><td><span class="type-chip">Number</span></td><td><code>character_level</code></td><td>Current character level.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="reference-section">
  <div class="section-heading">
    <div><p class="section-heading__eyebrow">Configuration rules</p><h2>Common field requirements</h2></div>
  </div>

  <div class="usage-action-grid">
    <article>
      <span>Names</span>
      <h3>Use exact Data Field values</h3>
      <p>Field names are case-sensitive. Do not add spaces, capitalization, or punctuation that is not shown in this reference.</p>
    </article>
    <article>
      <span>Types</span>
      <h3>Match the Presentation Type</h3>
      <p>A Number field must be configured as Number, an image field as Image, and <code>last_login</code> as Text.</p>
    </article>
    <article>
      <span>Publishing</span>
      <h3>Save and publish changes</h3>
      <p>After editing variables in Discord, select <strong>Save Changes</strong> and <strong>Publish</strong>, then run a WoWidget update.</p>
    </article>
  </div>
</section>

<aside class="ww-callout ww-callout--note"><strong>Available fields can evolve</strong><span>The variable set may expand as WoWidget adds new Blizzard data. Use the reference bundled with your current release when a field differs from an older screenshot or guide.</span></aside>
