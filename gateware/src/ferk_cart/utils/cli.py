from ferk_cart.platforms.homeinvader_rev_a import HomeInvaderRevAPlatform

def main_runner(fragment):
    platform = HomeInvaderRevAPlatform()
    platform.build(fragment, do_program=True)
    return fragment
