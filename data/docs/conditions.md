# Characteristics to Conditions

## Abilities
### Rend (Ex)
* Condition "Rend". Will deal 2d6+9 if target, attack description, round coincide.

### Resistance to [fire...]
* Condition "Monster Energy Resistance"

### Immunity to [electricity...]
* Condition "Monster Energy Immunity"

### Plant Traits | Plant Type
* Condition "Monster Plant"

### Regeneration (Ex)
* Condition "Monster Regeneration 5", heals 5 subdual, converts all damage type to subdual, except arg0 and arg1, default to Fire and Acid;
* Condition "Monster Regeneration 2", heals 2 subdual, converts all damage type to subdual, except arg0 and arg1, default to Fire and Acid;
* Condition "Monster Regeneration 1", heals 1 subdual, converts all damage type to subdual, except arg0 and arg1, default to Fire and Acid;

### Spell Resistance (Ex)
* Condition "Monster Spell Resistance", Arg0 (SR)

### Single Actions Only (Ex)
* Condition "Monster Zombie", 0 args;


## Conditions
### Rend
**Args** - **none**
Will deal 2d6+9 if target, attack description, round coincide.

### Monster Damage Type
**Args**
* Arg0: damage_type, like D20DT_BLUDGEONING etc
temple.dll::ConditionMonsterDamageType

### Monster Bonus Damage
**Args**
* Arg0: damage_type, like D20DT_BLUDGEONING etc
* Arg1: damage_dice_packed_
temple.dll::ConditionMonsterBonusDamage

### Monster Energy Resistance
**Args**
* Arg0: damage_amount
* Arg1: damage_type, like D20DT_BLUDGEONING etc

### Monster Energy Immunity
**Args**
* Arg0: damage_type, like D20DT_BLUDGEONING etc

### Monster Regeneration 5
**Args**
* Arg0: damage_type, default D20DT_FIRE
* Arg1: damage_type, default D20DT_ACID
If damage type is not of arg0 and arg1, then damage type is converted to subdual. Each round heals 5 subdual damage.

### Monster Regeneration 2
**Args**
* Arg0: damage_type, default D20DT_FIRE
* Arg1: damage_type, default D20DT_ACID
If damage type is not of arg0 and arg1, then damage type is converted to subdual. Each round heals 2 subdual damage.

### Monster Regeneration 1
**Args**
* Arg0: damage_type, default D20DT_FIRE
* Arg1: damage_type, default D20DT_ACID
If damage type is not of arg0 and arg1, then damage type is converted to subdual. Each round heals 1 subdual damage.

### Monster Spell Resistance
**Args**
* Arg0: Spell Resistance Level

### Monster Zombie
**Args** - none
Allow only single action.

### Monster Plant
**Args** - none
* Immunity to all mind-affecting effects (charms, compulsions, phantasms, patterns, and morale effects).
* Immunity to poison, sleep effects, paralysis, polymorph, and stunning.
* Not subject to critical hits.
temple.dll::condMonsterPlant

### Monster Untripable
**Args** - none
Disallow being tripped.
temple.dll::condMonsterUntripable

### Monster Incorporeal
**Args** - none
Incorporeal Immunity.
temple.dll::ConditionMonsterIncorporeal / MonsterIncorporealDamageCallback

### Monster Fast Healing
**Args**
* Arg0: DicePacked, heal each round.
temple.dll::stru_102EC590

### Monster Subdual Immunity
**Args** - none
Immune to subdual damage type.
temple.dll::ConditionMonsterSubdualImmunity

### Monster Special Fade Out
**Args** - none
* Immune to subdual damage type.
* Monster kill when HP <= 0
temple.dll::ConditionMonsterSpecialFadeOut

### Monster Confusion Immunity
**Args** - none
Immune to confusion.
temple.dll::stru_102EC6C0

### Monster Stable
**Args** - none
Stability bonus (against Trip) +4.
temple.dll::stru_102EC37C

### Paralyzed
**Args**
* Arg0: round remaining
Paralized condition.
temple.dll::condParalyzed

### Saving Throw Resistance Bonus
**Args** - 2
* Arg0: saving throw (for ex saving_throw_fortitude)
* Arg1: bonus
Adds saving throw resistance bonus.

todo:
pCondition_Monster_Banshee_Charisma_Drain
.data:102EC724 30 B7 2E 10      dd offset ConditionMonsterStirge
.data:102EC728 F0 B7 2E 10      dd offset ConditionMonsterFireBats
.data:102EC72C B0 B8 2E 10      dd offset ConditionMonsterMeleeDisease
.data:102EC730 08 B9 2E 10      dd offset ConditionMonsterMeleePoison
.data:102EC734 60 B9 2E 10      dd offset ConditionMonsterCarrionCrawler
.data:102EC738 A8 B9 2E 10      dd offset ConditionMonsterMeleeParalysis
.data:102EC73C 18 BA 2E 10      dd offset ConditionMonsterMeleeParalysisNoElf
.data:102EC754 F8 BC 2E 10      dd offset ConditionMonsterSalamander
.data:102EC758 50 BD 2E 10      dd offset ConditionMonsterOozeSplit
.data:102EC75C A8 BD 2E 10      dd offset ConditionMonsterSplitting
.data:102EC760 F0 BD 2E 10      dd offset ConditionMonsterJuggernaut
.data:102EC768 F8 BF 2E 10      dd offset ConditionMonsterSmiting
.data:102EC770 80 C0 2E 10      dd offset ConditionMonsterLamia
.data:102EC774 B0 C0 2E 10      dd offset stru_102EC0B0
.data:102EC778 08 C1 2E 10      dd offset stru_102EC108
.data:102EC77C 60 C1 2E 10      dd offset MonsterDrMagic
.data:102EC780 B8 C1 2E 10      dd offset MonsterDrAll
.data:102EC784 10 C2 2E 10      dd offset stru_102EC210
.data:102EC788 68 C2 2E 10      dd offset stru_102EC268
.data:102EC78C 4C C3 2E 10      dd offset stru_102EC34C
.data:102EC794 6C C4 2E 10      dd offset condMonsterUntripable
.data:102EC798 B0 C3 2E 10      dd offset condMonsterPlant
.data:102EC79C 9C C4 2E 10      dd offset stru_102EC49C
.data:102EC7A0 D0 C4 2E 10      dd offset conditionMonsterSpider
.data:102EC7A4 14 C5 2E 10      dd offset ConditionMonsterIncorporeal
.data:102EC7A8 48 C5 2E 10      dd offset ConditionMonsterMinotaurCharge
.data:102EC7B0 D8 C5 2E 10      dd offset stru_102EC5D8
.data:102EC7B4 C0 C2 2E 10      dd offset stru_102EC2C0
.data:102EC7B8 08 C3 2E 10      dd offset stru_102EC308
