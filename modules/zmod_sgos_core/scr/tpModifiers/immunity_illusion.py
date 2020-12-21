import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Illusion"

print("Registering " + GetConditionName())
###################################################

def Immunity_Illusion_OnSpellImmunityCheck(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjImmunityQuery)
	#print("Immunity_Illusion_OnSpellImmunityCheck")

	#spell_entry = evt_obj.spell_entry
	spell_enum = evt_obj.spell_packet.spell_enum
	#print("evt_obj.spell_packet.spell_enum: {}".format(spell_enum))
	if (not spell_enum): return 0

	spell_entry = tpdp.SpellEntry(spell_enum)
	#print(spell_entry)
	if (not spell_entry): return 0
	#print("spell_enum: {}, spell_school_enum: {}, spell_subschool_enum: {}, descriptor: {}".format(spell_entry.spell_enum, spell_entry.spell_school_enum, spell_entry.spell_subschool_enum, spell_entry.descriptor))

	if (spell_entry.spell_school_enum == (toee.D20STD_F_SPELL_SCHOOL_ILLUSION - toee.D20STD_F_SPELL_SCHOOL_ABJURATION + 1)):
		attachee.float_text_line( "Illusion Affecting Immunity", toee.tf_red)
		evt_obj.return_val = 1
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnSpellImmunityCheck, toee.EK_NONE, Immunity_Illusion_OnSpellImmunityCheck, ())
#breakp("Registered " + GetConditionName())
