import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Visual"

print("Registering " + GetConditionName())
###################################################

def Immunity_Visual_OnSpellImmunityCheck(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjImmunityQuery)
	#print("Immunity_Visual_OnSpellImmunityCheck")

	spell_enum = evt_obj.spell_packet.spell_enum
	#print("evt_obj.spell_packet.spell_enum: {}".format(spell_enum))
	if (not spell_enum): return 0

	spell_entry = tpdp.SpellEntry(spell_enum)
	#print(spell_entry)
	if (not spell_entry): return 0
	#print("spell_enum: {}, spell_school_enum: {}, spell_subschool_enum: {}, descriptor: {}".format(spell_entry.spell_enum, spell_entry.spell_school_enum, spell_entry.spell_subschool_enum, spell_entry.descriptor))

	if (spell_entry.descriptor & (1<<(toee.D20STD_F_SPELL_DESCRIPTOR_LIGHT-toee.D20STD_F_SPELL_DESCRIPTOR_ACID))):
		attachee.float_text_line( "Visual Affecting Immunity", toee.tf_red)
		evt_obj.return_val = 1
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnSpellImmunityCheck, toee.EK_NONE, Immunity_Visual_OnSpellImmunityCheck, ())
#breakp("Registered " + GetConditionName())
