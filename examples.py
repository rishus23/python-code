import FBpoker
import getpass

###simple one time poke###
# create the autoPoker
myPoker = FBpoker.autoPoker("email@example.com", "password")

# if the login is valid (good idea to always check this)
if myPoker.loggedin:

    # create a new user. user(userid, name, poke count)
    pokeTarget = FBpoker.user("4", "Mark Zuckerberg", "0")

    # poke the new user
    myPoker.pokeUser(pokeTarget)

else:
    print("Unable to login")


###continuous auto poking###
# create the autoPoker
myPoker = FBpoker.autoPoker(input("Username: "), getpass.getpass())

# if the login is valid (good idea to always check this)
if myPoker.loggedin:

    # create a user to blacklist. user(userid, name, poke count)
    blacklistUser = FBpoker.user("4", "Mark Zuckerberg", "0")

    # add the user to the blackList
    myPoker.addToBlacklist(blacklistUser)

    print("Waiting to poke:")

    # loop forever
    while True:

        # get the ids of people who have poked you
        myPoker.getPokeIds()

        # poke those users back
        usersPoked = myPoker.pokeUsersBack()

        # print the users poked
        for user in usersPoked:

            # print the user name & id and number of pokes.
            print(
                "Poked " + user.name + " (" + user.id + ") " + user.count + " times.")

else:
    print("Unable to login")
