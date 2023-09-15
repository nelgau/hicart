from hicart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform

def main_runner(fragment, do_program=False):
    platform = HomeInvaderRevAPlatform()
    platform.build(fragment, do_program=do_program)
    return fragment
