# Trap API
## Usage
The Container with Trap must have san_trap specified with counters, like "6203 12 0 0 0". First counter points to **trap_id**.
The implementation of the Trap must be coded in the san_trap event.


## toee.exe
### Search Trap
Trap_10051250

| name                 | trigger | flags          | particle       | search dc | disable dc | replace with | dmg 1-5       | cr | id |
|----------------------|---------|----------------|----------------|-----------|------------|--------------|---------------|----|----|
| TRAP_POISON_GAS      | san_use |                | Trap-poisonGas | 31        | 26         | TRAP_NONE    | poison 0d0+31 | 1  | 1  |
| TRAP_FIRE_TRAP_SPELL | san_use | TRAP_F_MAGICAL | Trap-Fire      | 31        | 31         | TRAP_NONE    | fire 1d4+10   | 1  | 6  |
| TRAP_SCYTHE          | san_use |                | Trap-Scythe    | 21        | 18         | TRAP_NONE    | Slashing 2d4  | 1  | 8  |

The Trap definition has following fields:
* id, - identifier of the specification.
* name, - internal name of the specification.
* flags, - the following: TF_IN_STONE, TF_PC, TF_SPOTTED, TF_MAGICAL.
* particle, - particle effect name.
* search dc.
* disable dc.
* replace with, - If the obj is not a "real" trap, the trap script will be replaced by this trap after triggering (by name)
* cr, - critter rating, for the XP.
* dmg1-5, - five different damage specifications.

The damage specifications for traps are obsolete and must be replaced by Python event hook of type "san_trap".

A Trap instance cannot be created manually by a game designer, but have to be setup on a portal (door) or chest.

A Trap Setup is specified in Holder's Scripts \ san_trap field using following syntax: "script_id trap_spec_id 0 0 0".

For example see proto 1001 "Treasure Chest", it has san_trap specified as: "32007 8 0 0 0". Here you can see that the Treasure Chest object has Trap setup. The Trap Specification ID is 8, which is TRAP_SCYTHE in the specifications file. The Trap would be triggered when the Chest will be used, and the execution of the Trap would be defined in Python script 32007, which corresponds to file "py32007Trap8_scythe.py".

The Trap Setup Syntax uses extended format of san script, which aside of script_id also includes Counters (0-4). These are treated as additional arguments of a script. In case of a Trap it is Counter 0.

Therefore, if one would rather define Trap Setup in the ToEE World Editor, he should use Counter 0 in Script Dialog as Trap Specification ID.