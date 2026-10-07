<img src="assets/icon.svg" width="64" height="64" alt="">

# Model-Comparison-Pixel-Fishing-Game

I tested several models through OpenCode Go's subscription, and this is all that they had to offer following the same prompt as a one-shot.

Each model was asked to build a Stardew Valley style fishing game as a single HTML file. The full prompt is in [PROMPT.md](PROMPT.md). The first six ran at the same time on 3 October 2026. Haiku 5.5 High 1M was added afterwards and ran separately on 7 October 2026.

Created in [T3 Code](https://t3.codes).

## Results

Each game is scored out of 25 on four things: creativity, design and visuals, enjoyability, and how good its one extra feature is. That makes 100 points in total.

| Model | Game | Total | Creativity | Design | Enjoyability | Feature | Time | Cost |
|---|---|---|---|---|---|---|---|---|
| [Grok 4.7 High](games/Grok_-4_7-high.html) | Stillwater | **73** | 19 | 18 | 14 | 22 | 38+ min | $1.22 |
| [Haiku 5.5 High 1M](games/Haiku-5_5-high-1M.html) | Pixel Pond | **45** | 14 | 15 | 10 | 6 | 6 min 49 s | $0.07 |
| [Grok 4.6 High](games/Grok-4_6-high.html) | Willow Pond | **33** | 13 | 7 | 6 | 7 | 5 min | $0.39 |
| [Luna 6 High](games/6-Luna-high.html) | Moonwake | **29** | 11 | 4 | 7 | 7 | 2 min | $0.007 |
| [LongCat Preview 2.5](games/Longcar-2_5.html) | Longcar-2.5 Pixel Pond Fishing | **26** | 8 | 8 | 3 | 7 | 21 min | free tier |
| [MiniMax M3 Thinking](games/MiniMax-M3-Thinking.html) | Pixel Fishing | **5** | 0 | 5 | 0 | 0 | 7 min | $0.06 |
| [GLM 5.3 High](games/GLM-5_3-high.html) | GONE FISHIN' | **0** | 0 | 0 | 0 | 0 | 27 min | $1.09 |

Grok 4.7 High looped for 32 minutes, needed steering, ran for 6 more minutes, looped again and then hit the 5 hour usage cap. Its time is a floor, and it is scored on what it produced. Together the six runs used 100% of the 5 hour allowance, and Grok 4.7 High alone used about 12% of it.

Costs for the first six come from the OpenCode request log and are API-equivalent dollars. They only cover the runs in this test.

## Notes on each game

- **Grok 4.7 High**: the best by a wide margin. It has sound, decent gameplay and decent visuals, and the most realistic dog of the group. Its extra mechanic is a bait box that adds progression. It is very hard, and the second and third bait tiers are harder still. It has a fail condition.
- **Haiku 5.5 High 1M**: really good for the price, at $0.07 for the prompt and 6 min 49 s. I think it is at its best when given a good enough prompt, where it can really excel, but it needs guidance. This is from my testing so far.
- **Grok 4.6 High**: its extra mechanic is a fish log. It is very hard and has sound. The visuals are poor but not blurry. The dog is hard to recognise as a dog.
- **Luna 6 High**: the UI is very blurry and sometimes hard to read. It has a fail condition but nothing especially interesting. It is not bad for the price and speed.
- **LongCat Preview 2.5**: also a fish log. The fish is hidden behind the catch bar, and you have to be on it within a second or you fail. The dog is a shapeless blob.
- **MiniMax M3 Thinking**: only the home screen works. A bait box is mentioned but nothing else runs. The pixel art is weak and there is no recognisable dog.
- **GLM 5.3 High**: fully broken. It shows a blank screen with a black box in the centre.

## Slides

The comparison charts are in [slides/index.html](slides/index.html): how long each model took, time against quality, and what each run cost. The Fable 5.1, GPT Astra and Gemini 2.5 Pro bars on the time and cost slides are illustrative estimates for reference, not measured runs.

## Running things

Every game is a single self-contained HTML file. Open any file in `games/` in a browser. To browse them all, open `index.html`, or enable GitHub Pages for this repository.

## Repository layout

```
index.html            landing page linking to every game
PROMPT.md             the exact prompt every model received
games/                one HTML file per model, exactly as the model returned it
slides/index.html     the three comparison slides (generated)
data/results.json     times, scores and costs used by the slides
scripts/build_slides.py   rebuilds slides/index.html and index.html from the data
assets/icon.svg
```

To change a score or a cost, edit `data/results.json` and run:

```
python3 scripts/build_slides.py
```

## Notes

- The raw OpenCode request log is not included because it contains account and location details.
