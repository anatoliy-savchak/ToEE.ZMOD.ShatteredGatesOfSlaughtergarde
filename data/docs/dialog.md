# DLG
## Format
`{line_id}{text}{text female}{min IQ}{test field|speech_id}{answer key}{effect python}`

* **line_id_**, required, unique.
* **text**, required, length unlimited.
* **text female**, optional, length unlimited.
* **min IQ**, required, applies only for PC lines.
* **test field**, optional, applies only for PC lines.
* **speech_id**, optional, applies only for NPC lines.
* **answer key**, optional, applies only for PC lines.
* **effect python**, optional, applies only for PC lines.

## Samples
`{1}{NPC text}{}{}{}{}{}`
`{2}{PC answer 1}{}{1}{}{4}{}`
`{3}{PC answer 2}{}{1}{}{4}{}`
`{4}{NPC text 2}{}{}{}{}{}`
`{5}{[exit]}{}{1}{}{}{}`

Looks like:
NPC text
1. PC answer 1
2. PC answer 2

NPC text 2
1. Exit

A: - Many thanks good sir!
F: I have changed my mind, sir.

## Notes
line_id must be consecutive!!