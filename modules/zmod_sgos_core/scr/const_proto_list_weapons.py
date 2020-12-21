import const_proto_weapon

PROTOS_WEAPON_SIMPLE_MELEE_LIGHT = [\
	const_proto_weapon.PROTO_WEAPON_DAGGER \
	, const_proto_weapon.PROTO_WEAPON_DAGGER_THROWING \
	, const_proto_weapon.PROTO_WEAPON_MACE_LIGHT \
	, const_proto_weapon.PROTO_WEAPON_SICKLE \
	]

PROTOS_WEAPON_SIMPLE_MELEE_ONE_HANDED = [\
	const_proto_weapon.PROTO_WEAPON_CLUB \
	, const_proto_weapon.PROTO_WEAPON_MACE_HEAVY \
	, const_proto_weapon.PROTO_WEAPON_MORNINGSTAR \
	, const_proto_weapon.PROTO_WEAPON_SHORTSPEAR \
	]

PROTOS_WEAPON_SIMPLE_MELEE_TWO_HANDED = [\
	const_proto_weapon.PROTO_WEAPON_LONGSPEAR \
	, const_proto_weapon.PROTO_WEAPON_QUARTERSTAFF \
	, const_proto_weapon.PROTO_WEAPON_SPEAR \
	]

PROTOS_WEAPON_SIMPLE_MELEE = PROTOS_WEAPON_SIMPLE_MELEE_LIGHT + PROTOS_WEAPON_SIMPLE_MELEE_ONE_HANDED + PROTOS_WEAPON_SIMPLE_MELEE_TWO_HANDED

PROTOS_WEAPON_SIMPLE_RANGED = [\
	const_proto_weapon.PROTO_WEAPON_CROSSBOW_HEAVY \
	, const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT \
	, const_proto_weapon.PROTO_AMMO_BOLT_QUIVER \
	, const_proto_weapon.PROTO_WEAPON_JAVELIN \
	, const_proto_weapon.PROTO_WEAPON_DART \
	, const_proto_weapon.PROTO_WEAPON_SLING \
	, const_proto_weapon.PROTO_AMMO_BULLET_POUCH \
	]

PROTOS_WEAPON_SIMPLE = PROTOS_WEAPON_SIMPLE_MELEE + PROTOS_WEAPON_SIMPLE_RANGED

PROTOS_WEAPON_MARTIAL_MELEE_LIGHT = [\
	const_proto_weapon.PROTO_WEAPON_HAMMER_LIGHT \
	, const_proto_weapon.PROTO_WEAPON_HANDAXE \
	, const_proto_weapon.PROTO_WEAPON_KUKRI \
	, const_proto_weapon.PROTO_WEAPON_SICKLE \
	, const_proto_weapon.PROTO_WEAPON_SHORTSWORD \
	] # missing: Throwing Axe, Light Pick, Sap

PROTOS_WEAPON_MARTIAL_MELEE_ONE_HANDED = [\
	const_proto_weapon.PROTO_BATTLEAXE \
	, const_proto_weapon.PROTO_FLAIL \
	, const_proto_weapon.PROTO_LONGSWORD \
	, const_proto_weapon.PROTO_WEAPON_PICK_HEAVY \
	, const_proto_weapon.PROTO_RAPIER \
	, const_proto_weapon.PROTO_SCIMITAR \
	, const_proto_weapon.PROTO_WEAPON_TRIDENT \
	, const_proto_weapon.PROTO_WEAPON_WARHAMMER \
	]

PROTOS_WEAPON_MARTIAL_MELEE_TWO_HANDED = [\
	const_proto_weapon.PROTO_WEAPON_FALCHION \
	, const_proto_weapon.PROTO_WEAPON_GLAIVE \
	, const_proto_weapon.PROTO_WEAPON_GREATAXE \
	, const_proto_weapon.PROTO_WEAPON_GREATCLUB \
	, const_proto_weapon.PROTO_WEAPON_FLAIL_HEAVY \
	, const_proto_weapon.PROTO_WEAPON_GREATSWORD \
	, const_proto_weapon.PROTO_WEAPON_GUISARME \
	, const_proto_weapon.PROTO_WEAPON_HALBERD \
	, const_proto_weapon.PROTO_WEAPON_RANSEUR \
	, const_proto_weapon.PROTO_WEAPON_SCYTHE \
	] # missing: Lance

PROTOS_WEAPON_MARTIAL_MELEE = PROTOS_WEAPON_MARTIAL_MELEE_LIGHT + PROTOS_WEAPON_MARTIAL_MELEE_ONE_HANDED + PROTOS_WEAPON_MARTIAL_MELEE_TWO_HANDED

PROTOS_WEAPON_MARTIAL_RANGED = [\
	const_proto_weapon.PROTO_WEAPON_LONGBOW \
	, const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_12 \
	, const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_14 \
	, const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_16 \
	, const_proto_weapon.PROTO_WEAPON_SHORTBOW \
	, const_proto_weapon.PROTO_AMMO_ARROW_QUIVER \
	] # missing: Shortbow Composite

PROTOS_WEAPON_MARTIAL = PROTOS_WEAPON_MARTIAL_MELEE + PROTOS_WEAPON_MARTIAL_RANGED

PROTOS_WEAPON_EXOTIC_MELEE_LIGHT = [\
	const_proto_weapon.PROTO_WEAPON_SPIKED_KAMA \
	, const_proto_weapon.PROTO_WEAPON_SPIKED_SIANGHAM \
	] # missing: Nunchaku, Sai

PROTOS_WEAPON_EXOTIC_MELEE_ONE_HANDED = [\
	const_proto_weapon.PROTO_WEAPON_SWORD_BASTARD \
	, const_proto_weapon.PROTO_WEAPON_WARAXE_DWARVEN \
	] # missing: Whip

PROTOS_WEAPON_EXOTIC_MELEE_TWO_HANDED = [\
	const_proto_weapon.PROTO_WEAPON_DOUBLEAXE_ORC \
	, const_proto_weapon.PROTO_WEAPON_SPIKED_CHAIN \
	, const_proto_weapon.PROTO_WEAPON_HAMMER_GNOME_HOOKED \
	] # missing: Dire Flail, Two-bladed Sword, Urgrosh

PROTOS_WEAPON_EXOTIC_MELEE = PROTOS_WEAPON_EXOTIC_MELEE_LIGHT + PROTOS_WEAPON_EXOTIC_MELEE_ONE_HANDED + PROTOS_WEAPON_EXOTIC_MELEE_TWO_HANDED

PROTOS_WEAPON_EXOTIC_RANGED = [\
	const_proto_weapon.PROTO_WEAPON_CROSSBOW_REPEATING_LIGHT \
	, const_proto_weapon.PROTO_WEAPON_SHURIKEN \
	] # missing: Bolas, Hand Crossbow, Repeating Heavy Crossbow, Net

PROTOS_WEAPON_EXOTIC = PROTOS_WEAPON_EXOTIC_MELEE + PROTOS_WEAPON_EXOTIC_RANGED