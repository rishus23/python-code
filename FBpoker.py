# coding=utf-8
from __future__ import unicode_literals, print_function
import requests

# class for the users for the auto poker


class user(object):

    def __init__(self, id, name, count=0):
        self.id = id
        self.name = name
        self.count = count

# class for error messages


class error(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

# class for the autoPoker


class autoPoker(object):

    headVars = {
        "HOST": "m.facebook.com",
        "User-Agent" : '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0)
            Gecko/20100101 Firefox/33.0''',
        "Accept" : '''text/html,application/xhtml+xml,application/
            xml;q=0.9,*/*;q=0.8'''
    }

    # create the autoPoke instance
    def __init__(self, email, password):

        # create a blank blacklist
        self.blacklist = list()

        # create a blank target list
        self.pokeTargets = list()

        # create a session using requests to keep track of cookies/sessions
        self.session = requests.session()

        # header variables that we need, without these we cannot login
        hdr = {
            "POST": "/login.php?refsrc=https://m.facebook.com/home.php",
            "HOST": self.headVars["HOST"],
            "User-Agent": self.headVars["User-Agent"],
            "Accept": self.headVars["Accept"]
        }

        # all we need is the email/password of the user for data
        data = {
            "email": email,
            "pass": password
        }

        # homepage data
        homepg = self.session.post("https://m.facebook.com/login.php",
                                   headers=hdr, data=data)

        # if the user has two factor enabled
        if homepg.url[0:33] == "https://m.facebook.com/checkpoint":

            firthAuth = homepg.text

            print("You have two factor authorization enabled.")

            firstTimeAuth = True

            # while we are on the security code page
            while "Please enter the security code" in firthAuth:

                if firstTimeAuth == False:
                    print("Incorrect authorization code.")
                else:
                    firstTimeAuth = False

                authMessage = "Please enter your two factor authorization code:"

                # python2.x
                try:
                    authCode = raw_input(authMessage)

                # python3.x
                except NameError:
                    authCode = input(authMessage)

                # in mobile
                auth_nh = firthAuth.split('nh" value="')[1].split('"')[0]
                auth_lsd = firthAuth.split('lsd" value="')[1].split('"')[0]

                authData1 = {

                    "nh": auth_nh,
                    "codes_submitted": "0",
                    "approvals_code": authCode,
                    "charset_test": "€,´,€,´,水,Д,Є",
                    "lsd": auth_lsd,
                    "submit[Submit Code]": "Submit Code",
                }

                # header for auth
                authHdr = {
                    "POST": "/login/checkpoint/",
                    "HOST": self.headVars["HOST"],
                    "User-Agent": self.headVars["User-Agent"],
                    "Accept": self.headVars["Accept"]
                }

                checkpointURL = "https://www.facebook.com/checkpoint/"

                # request for the security code
                secondAuthPage = self.session.post(checkpointURL,
                                                   headers=authHdr,
                                                   data=authData1)

                firthAuth = secondAuthPage.text

            # once we get the security code correct

            authData2 = {
                "name_action_selected": "dont_save",
                "submit[Continue]": "Continue",
                "lsd": auth_lsd,
                "nh": auth_nh,
                "charset_test": "€,´,€,´,水,Д,Є"
            }

            checkpointURL = "https://www.facebook.com/checkpoint/"

            # request for the login save
            ThirdAuthPage = self.session.post(checkpointURL, headers=authHdr,
                                              data=authData2)

            # restore var names for rest of code
            homepg = ThirdAuthPage
        # end of auth case

        # case for login review
        if "Review Recent Login" in homepg.text:

            reviewPage = homepg.text

            # get the values for the post request
            review_nh = reviewPage.split('nh" value="')[1].split('"')[0]
            review_lsd = reviewPage.split('lsd" value="')[1].split('"')[0]

            reviewData1 = {

                "nh": review_nh,
                "charset_test": "€,´,€,´,水,Д,Є",
                "lsd": review_lsd,
                "submit[Continue]": "Continue",
            }

            # header for auth
            reviewHdr = {
                "POST": "/login/checkpoint/",
                "HOST": self.headVars["HOST"],
                "User-Agent": self.headVars["User-Agent"],
                "Accept": self.headVars["Accept"]
            }

            checkpointURL = "https://www.facebook.com/checkpoint/"

            # request for the login review code
            secondReview = self.session.post(checkpointURL, headers=reviewHdr,
                                             data=reviewData1)

            reviewData2 = {
                "nh": review_nh,
                "charset_test": "€,´,€,´,水,Д,Є",
                "lsd": review_lsd,
                "submit[This is Okay]": "This is Okay",
            }

            thirdReview = self.session.post(checkpointURL, headers=reviewHdr,
                                            data=reviewData2)

            # doesn't always ask to remember
            if "Remember Browser" in thirdReview.text:

                reviewData3 = {
                    "name_action_selected": "dont_save",
                    "submit[Continue]": "Continue",
                    "lsd": review_lsd,
                    "nh": review_nh,
                    "charset_test": "€,´,€,´,水,Д,Є"
                }

                # final request to get to the homepage
                homepg = self.session.post(checkpointURL, headers=reviewHdr,
                                           data=reviewData3)
        # end of login review case

        homepg = homepg.text

        # split up the text to get the digest and current user id
        homepg_dtsg = homepg.split("fb_dtsg")
        homepg_userid = homepg.split(
            '<input type="hidden" name="target" value="')

        # if we have logged in
        if len(homepg_dtsg) > 1:

            # set the login flag
            self.loggedin = True

            # set the facebook digest
            self.fb_dtsg = homepg_dtsg[1][9:21]

            # set the user id
            self.user_id = homepg_userid[1].split('"')[0]

        # if we did not login correctly
        else:

            # set the login flag
            self.loggedin = False

    # get the users who need to be poked
    def getPokeIds(self):

        # make sure we are logged in
        if(self.loggedin):

            # request the page
            pokePage = self.session.get("https://m.facebook.com/pokes")

            # create an empty list
            pokeTargets = list()

            # split up the text to get the ids
            idFind = pokePage.text.split('id="poke_live_item_')

            # split up the text to get the names
            nameFind = pokePage.text.split('" alt="')[1:]

            # split up to find number of pokes
            countFind = pokePage.text.split("poked you ")

            # go through each id and add them to postTargets
            for item in range(1, len(idFind)):

                # get the user to be poked id
                pokeId = idFind[item].split('"')[0]

                # get the count of pokes
                try:
                    pokeCount = countFind[item].split(" ")[0]

                # if the poke count can't be found, the count is 1
                except:
                    pokeCount = 1

                # get the user to be poked name
                pokeName = nameFind[item].split('"')[0]

                # create a new poke target user
                pokeTarget = user(pokeId, pokeName, pokeCount)

                # set the blackList bool
                onBlacklist = False

                # go throught to see if it is in blacklist
                for buser in self.blacklist:

                    # if the user is on the blacklist change the bool
                    if buser.id == pokeTarget.id:
                        onBlacklist = True

                # if the user is someone we want to poke back
                if not onBlacklist:

                    # add the target to the array
                    pokeTargets.append(pokeTarget)

            # assign poke targets array
            self.pokeTargets = pokeTargets

            return pokeTargets

    # poke a single user
    def pokeUser(self, poke_target):

        # set the blackList bool
        onBlacklist = False

        # go throught to see if it is in blacklist
        for buser in self.blacklist:

            # if the user is on the blacklist change the bool
            if buser.id == poke_target.id:
                onBlacklist = True

        # if the user is not on the blacklist and logged in
        if not onBlacklist and self.loggedin:

            # input for the poke
            data = ("__a=1&poke_target=" + poke_target.id + "&__user=" +
                    self.user_id +
                    "&__dyn=7n8ajEyl35zoSt2u6aWizGomyp9ErghyWgSmEV"
                    + "FLFwxBxCbzESu48jhHximmey8szoyfw&fb_dtsg=" + self.fb_dtsg)

            # make the post request
            response = self.session.post("https://www." +
                                         "facebook.com/pokes/inline/",
                                         data=data).text

            # if the user we want to poke is in the pokeTargets
            if poke_target in self.pokeTargets:

                # remove that id from the poke targets
                self.pokeTargets.remove(poke_target)

            # get error messages (if there is one)
            error = response[27:34]

            # if the user has already been poked
            if error == "1769004":
                pokeError = error("1769004", "Already Poked")
                return pokeError

            # if the user is not allowed to be poked
            elif error == "1769005":
                pokeError = error("1769005", "Unauthorized Poke")
                return pokeError

            # if there is another error
            elif response[20:25] == "error":
                pokeError = error("0000000", "Unknown Error")
                return pokeError

            # if there are no errors, return the poke target
            return poke_target

    # poke all users back
    def pokeUsersBack(self):

        # create a list to return
        pokedList = list()

        # go though each of the ids in pokeTargets
        for user in self.pokeTargets:

            # poke that user
            self.pokeUser(user)

            # add the user to the pokedList
            pokedList.append(user)

        # return a list of users that were poked
        return pokedList

    # add user to the blacklist
    def addToBlacklist(self, poke_target):

        # add to the blacklist
        self.blacklist.append(poke_target)

    # remove user from the blacklist
    def removeFromBlacklist(self, poke_target):

        # if the user is in the blacklist
        if poke_target in self.blacklist:

            # remove the user
            self.blacklist.remove(poke_target)
