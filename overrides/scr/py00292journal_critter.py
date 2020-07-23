from toee import *

def san_dialog( attachee, triggerer ):
	triggerer.begin_dialog(attachee,1)
	return SKIP_DEFAULT

def how_many_marks():
	x = 0
	if game.global_flags[533] == 1:
		x += 1
	if game.global_flags[534] == 1:
		x += 1
	if game.global_flags[535] == 1:
		x += 1
	if game.global_flags[536] == 1:
		x += 1
	if game.global_flags[537] == 1:
		x += 1
	if game.global_flags[538] == 1:
		x += 1
	if game.global_flags[539] == 1:
		x += 1
	return x