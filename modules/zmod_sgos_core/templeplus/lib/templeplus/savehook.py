
#use 4 space indentation!

def save(filename):
    print "Executing ZMOD Save Hook"
    from utils_storage import Storage
    Storage.save(filename)
    return

def load(filename):
    print "Executing ZMOD Load Hook"
    from utils_storage import Storage
    Storage.load(filename)
    from startup_zmod import zmod_templeplus_config_apply
    zmod_templeplus_config_apply()
    return

# Co8 python save hook - executes after the archive is done
# save hook (default - Co8 hook; will silently fail for vanilla; feel free to change for your own custom mod!)
def post_save(filename):
    try:
        import _co8init
        print "imported Co8Init inside templeplus package"
        _co8init.save(filename)
        print "Co8 Save hook successful"
    except:
        print "Co8 Save hook failed\n"

# save hook (default - Co8 hook; will silently fail for vanilla; feel free to change for your own custom mod!)
def post_load(filename):
    try:
        import _co8init
        _co8init.load(filename)
    except:
        print "Co8 Load hook failed\n"