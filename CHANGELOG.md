# Evony Gear Optimizer — Changelog

All notable changes are documented here. Entries are written for users,
not developers — focused on what changed and why it matters.

---

## v1.3.0
**Profiles, Changelog**

- **Multiple profiles** — support for multiple named profiles, each with
  independent gear ownership, general assignments, and settings. Useful for
  players with multiple game accounts.
- **Profile selector** — after the splash screen, a profile chooser appears
  when more than one profile exists. The last-used profile is pre-selected
  with a 5-second auto-load countdown.
- **Profile management panel** — a slide-out Profiles panel in the header
  lets you create, rename, duplicate, switch, and delete profiles.
- **Duplicate profile** — copy an existing profile's gear ownership and
  general assignments to a new named profile, with a clear description of
  what will be copied before confirming.
- **Smooth profile switching** — switching profiles shows a "Switching to
  [Profile Name]..." overlay and reloads the app cleanly.
- **Changelog** — this changelog, accessible from the app header.

---

## v1.2.2
**Buff splitting improvements**

- **Combined buffs now split correctly** — buffs like "Ground Troop and
  Mounted Troop Attack +25%" are now split into individual entries
  (Ground Troop Attack, Mounted Troop Attack) so each scores independently
  against your scenario priorities. Previously these scored zero.
- **Multi-stat combined buffs** — buffs combining multiple troop types AND
  multiple stats (e.g. "Ground and Mounted Troop Attack and Defense on
  Monsters +30%") now expand to all combinations (4 entries in this case).
- **All Troops expansion** — "All Troops Attack", "Enemy Troop Defense",
  "Attacking Troops Attack" etc. now correctly expand to all four individual
  troop types (Ground, Mounted, Ranged, Siege Machine).
- **All Troops Load** — correctly expands to all four troop type Load buffs.
- **Monsters Attack and Defense** — correctly splits to Monsters Attack and
  Monsters Defense (monster enemy debuffs).
- **Set bonus buffs** — combined buff names in set bonuses are also split,
  not just individual piece buffs.
- **w/ Dragon spelling** — corrected inconsistent "w/Dragon" to "w/ Dragon"
  in the data file.

---

## v1.2.1
**Bug fixes and stability**

- **Data auto-sync fixed** — a critical bug caused data and settings to be
  written to a temporary folder that was deleted on exit. Settings now
  correctly persist to the install directory between sessions.
- **Startup log** — a startup.log file is created in the install folder
  for troubleshooting data sync issues.
- **Sync Data button** — a manual "⬇ Sync Data" button added to the header
  for on-demand data file updates from GitHub.
- **Asset naming fixed** — the data file now uploads to GitHub with the
  correct filename, ensuring auto-sync works for all users.
- **Sub-City Development scenarios** — "Construction Speed", "Gold
  Production Speed", and "Training Speed" sub-types now resolve correctly
  instead of showing "Scenario not found".
- **Generals sheet updated** — revised column layout with new
  "Covenant Generals" column and updated headers.
- **Graceful update check** — the Updates button no longer shows an error
  when no releases have been published yet.

---

## v1.2.0
**Splash screen, GitHub integration, civ gear category toggles**

- **Splash screen** — a native loading screen appears immediately on launch,
  showing progress while the app initializes. No more staring at a blank
  screen during startup.
- **Data caching** — gear data is loaded once at startup and cached in
  memory. Searches and reloads are significantly faster.
- **Automatic data updates** — the app silently checks for an updated data
  file on GitHub at each startup and replaces the local copy if a newer
  version is available.
- **Software update check** — checks for new software versions every 7 days
  or 10 startups. A notification appears if an update is available, with a
  link to download it.
- **⟳ Updates button** — manually check for a new software version at any
  time from the header.
- **Conquest / Supremacy toggles** — two toggle buttons in the Advanced Gear
  Owned section let you select or clear all Conquest pieces (Helmet, Ring,
  Leg Armor) or all Supremacy pieces (Armor, Weapon, Boots) across all civ
  sets at once. Button color reflects current state: green = all selected,
  amber = all cleared, default = mixed.
- **Civ gear category column** — the Civilization Gear data sheet now
  includes a Category column (Conquest/Supremacy) at the piece level.
- **GitHub release script** — a github_release.py script automates
  publishing new releases to GitHub, including data-only updates
  (--data-only flag).

---

## v1.1.0
**Generals system, themes, contextual help, app icon**

- **Imperial Crimson theme** — a new color scheme matching the game's
  visual aesthetic: deep burgundy chrome and aged parchment content panels.
  Toggle between Classic (Imperial Crimson) and Noir in the header.
  Selection persists across sessions.
- **Generals system** — assign recommended gear sets to specific generals.
  Up to two named sets per general. Assigned civ pieces are automatically
  excluded from future recommendations.
- **View Generals screen** — see all generals with assigned gear, with
  per-piece unassign, per-set clear, and the ability to manually assign
  individual pieces to empty slots.
- **Left panel assignment indicators** — owned civ pieces show an amber ⚔
  badge with the assigned general's name when in use.
- **Contextual help** — question mark icons throughout the interface provide
  in-place explanations for every user-input section.
- **App icon** — shield and crossed swords motif on the desktop shortcut,
  taskbar, and window title bar.
- **Settings persistence** — settings now save to settings.json in the
  install folder, surviving browser changes and app reinstalls.
- **Data file renamed** — evony_gear_data.xlsx renamed to evony_data.xlsx
  to reflect its expanded scope.
- **Scoring attributes simplified** — the expandable attribute list is
  replaced with a clean count in the subtitle.

---

## v1.0.0
**Initial release**

- Gear recommendation engine for all PVP, PVE, Sub-City, and Development
  scenarios.
- Forge and Civilization gear support with ownership tracking.
- Apollo and Asura advanced forge gear support.
- Forge level filtering (20, 27, 30, 33+).
- 6-piece combination optimizer with set bonus calculation.
- Collective buff and debuff summary with weighted scoring.
- Compare view — side-by-side comparison of the recommendation against
  your current gear setup.
- All-options-by-slot ranked list showing every viable piece per slot.
- Gear ownership persisted across sessions.
