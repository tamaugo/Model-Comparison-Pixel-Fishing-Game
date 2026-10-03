# The prompt

Every model received this exact prompt and had one attempt (a one-shot).

---

Build me a complete, playable 2D fishing game inspired by the fishing minigame in Stardew Valley.

**PLATFORM**
- A single self-contained HTML file (HTML, CSS and JavaScript all in one file) that runs by opening it in a browser. No external libraries, images or assets. Draw all art in code.

**ART STYLE**
- 8-bit pixel art look. Use a low internal resolution (e.g. 320x180) scaled up with crisp pixels (no smoothing), a limited colour palette, and chunky sprites.

**SETTING**
- The player stands on the edge of a lake and fishes into a pond area of water in front of them. Make the scene feel like one cohesive location (shoreline, water, a bit of scenery).

**CORE MECHANIC: FISHING (this is the main focus)**
- Cast, wait for a bite, then play a skill-based reeling minigame similar to Stardew Valley's (e.g. keep a bobber/bar over a moving fish to fill a catch meter; lose progress if you miss).
- Include at least 8 different fish species with a mix of difficulties (e.g. easy, medium, hard, rare/legendary). Difficulty should visibly change how the fish behaves in the minigame (speed, erratic movement, etc.) and how rare it is.
- Show each catch with its name, a pixel sprite and its difficulty.

**ADDITIONAL FEATURES**
- A dog companion that is visible in the scene and reacts to what happens (for example, to casting, bites or catches).
- ONE extra mechanic of your own choice that complements the fishing (for example: selling fish, a bait system, a daily time/weather cycle, a collection log). Pick only one and tell me which one you chose.

**CONTROLS AND UI**
- Simple controls (keyboard and/or mouse), with on-screen instructions.
- A basic HUD showing what is needed (e.g. catches, score or money).

**OUTPUT**
- Give me the full code in one file, followed by a short note (2 to 3 sentences) naming the extra mechanic you chose and explaining how to play.
