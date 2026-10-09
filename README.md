# linkedin-ad-copy

A Claude skill for writing B2B LinkedIn ad copy. It tests different strategic bets rather than rewordings of one idea.

Given a positioning line, persona, differentiators and a few verbatim customer quotes, it:

1. Generates 8 distinct angles and cuts them to the 4-5 most different
2. Writes three hooks per angle that land inside LinkedIn's 140-character "see more" cut
3. Writes intro text, a headline, a 4-slide carousel outline and an angle-matched CTA
4. Specs a visual brief that matches each angle
5. Outputs a test matrix with a Learning column, plus launch advice

`scripts/check_copy.py` checks hook, intro and headline length plus banned words and openers before the copy ships.

## Install

Claude Code:

```bash
git clone https://github.com/aj-suresh/linkedin-ad-copy-skill ~/.claude/skills/linkedin-ad-copy
```

Or download the folder and upload it as a skill in Claude.ai.

## Use

Ask Claude something like: "Write LinkedIn ads for [product]. Positioning: ... Persona: ... Quotes: ..."

## Layout

- `SKILL.md`: the workflow and rules
- `references/frameworks.md`: AIDA, PAS, BAB, PASTOR, QUEST, StoryBrand, 4 Cs, 4 Us, FAB, Message Layers, awareness levels, Value Equation and more
- `scripts/check_copy.py`: copy checker (Python 3, no dependencies)

## Credits

The angle, hook and test-matrix method follows Get Wicked Growth's [LinkedIn ad creative playbook](https://www.getwickedgrowth.com/use-cases/linkedin-ad-creative-concepts/) by Vikash Koushik. The framework reference draws on Eugene Schwartz, Joanna Wiebe, Ray Edwards, Perry Marshall, Donald Miller, Alex Hormozi, April Dunford, Wynter, Chris Walker and Dave Gerhardt. This is an independent summary and is not affiliated with or endorsed by any of them.

The 140/600 character limits come from the playbook. The ~70 character headline guidance and the preset CTA button list come from general knowledge of LinkedIn and should be checked against current LinkedIn specs.

## License

MIT
