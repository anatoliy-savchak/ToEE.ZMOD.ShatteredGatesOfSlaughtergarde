# Portrait API
## Specifiction
Portrait for a NPC is referenced in proto's obj_f_critter_portrait field by number, which as rule, should end with zero, for example: 960.
Portraits are specified in this file: \art\interface\portraits\portraits.mes, and have following specification:

{key  }{portrait_big_130x150_pc_only.tga}
{key+1}{portrait_mini_42x37_initiative.tga}
{key+2}{portrait_small_53x47_follower_status_window.tga}
{key+3}{portrait_small_53x47_follower_status_window_dead.tga}
{key+4}{portrait_mini_42x37_initiative_dead.tga}

Tga options: 
origin - bottom left
compression - none (!)

Example for Wight:
{10000}{}
{10001}{npc_wight_42x37.tga}
{10002}{npc_wight_53x47.tga}
{10003}{npc_wight_53x47_grey.tga}
{10004}{npc_wight_42x37_grey.tga}

## Validation
1. First line could have no file.
2. All other 4 lines must be present and reference valid tga files.
3. Subfolders in art\portraits do not work.
4. override\art\interface\portraits\portraits.mes will work.
5. override\art\interface\portraits\ location for tga files would work.
6. RLE compression in tga will not work.

# GIMP
1. Create 42x37 or 53x47
2. Copy image, paste.
3. Use Tools\Transform Tools\Scale (Shift+S)
4. For grey - use Colors\Desaturate\Color to Grey... (Ctrl+G, reassigned)