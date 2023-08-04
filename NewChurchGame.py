import random
import os

class Beliefs:
    """
    This class represents the beliefs of an NPC. Each NPC has a belief level,
    an attitude, and a religion. The belief level probabilities are influenced 
    by the type of location where the NPC is found.
    """
    def __init__(self, location_type):
        belief_levels = ['Strong', 'Moderate', 'Weak']
        attitudes = ['Favorable', 'Neutral', 'Hostile']
        religions = ['None', 'Evangelist', 'Jehovah\'s Witness', 'Mormon', 'Custom', 'Satanic']

        # Adjust probabilities based on location type
        if location_type in ['Church']:
            belief_levels_weights = [0.6, 0.3, 0.1]
        elif location_type in ['School']:
            belief_levels_weights = [0.1, 0.2, 0.7]
        else:
            belief_levels_weights = [0.3, 0.4, 0.3]

        self.level = random.choices(belief_levels, weights=belief_levels_weights, k=1)[0]
        self.attitude = random.choice(attitudes)
        self.religion = random.choice(religions)


class NPC:
    """
    This class represents an NPC who may be converted by the player. 
    An NPC has a resistance to conversion, a record of failed conversion 
    attempts, and a set of beliefs.
    """
    def __init__(self, location_type):
        self.converted = False
        self.failed_attempts = 0
        self.resistant = random.choice([True, False])
        self.beliefs = Beliefs(location_type)

    def convert(self, player_religion, conversion_rate):
        """
        This method attempts to convert the NPC to the player's religion. The 
        success of the conversion is influenced by the NPC's current religion, 
        belief level, attitude, and a random factor. If the conversion is 
        successful, the NPC's religion is changed to the player's religion.
        """
        if self.beliefs.religion == player_religion:
            print("This person is already a follower of your religion.")
            return
        conversion_chance = conversion_rate
        if self.beliefs.level == 'Strong':
            conversion_chance *= 0.5
        elif self.beliefs.level == 'Weak':
            conversion_chance *= 2
        if self.beliefs.attitude == 'Favorable':
            conversion_chance *= 2
        elif self.beliefs.attitude == 'Hostile':
            conversion_chance *= 0.5
        self.converted = random.random() < conversion_chance
        if self.converted:
            self.beliefs.religion = player_religion


class Location:
    """
    This class represents a location that the player can visit. A location 
    has a type (House, Apartment, Park, School, Office, Café, Restaurant, 
    Shopping Center, Church, or Hospital) and a number of NPCs. If at least 
    ten NPCs at a location have been converted, the location becomes a church 
    of the player's religion.
    """
    location_types = ['House', 'Apartment', 'Park', 'School', 'Office', 
                      'Café', 'Restaurant', 'Shopping Center', 'Church', 'Hospital']

    def __init__(self, num_npcs):
        self.type = random.choice(Location.location_types)
        self.npcs = [NPC(self.type) for _ in range(num_npcs)]
        self.church = False
        self.church_religion = None

    def check_church_status(self, player_religion):
        """
        This method checks if the location has become a church of the player's religion.
        If at least ten NPCs at the location have been converted, the location becomes 
        a church of the player's religion.
        """
        if sum(npc.converted for npc in self.npcs) >= 10:
            self.church = True
            self.church_religion = player_religion

    def get_conversion_rate_multiplier(self):
        """
        This method calculates a conversion rate multiplier based on the proportion of 
        NPCs at the location that have been converted. The conversion rate multiplier 
        is 1 plus the proportion of converted NPCs.
        """
        num_converted = sum(npc.converted for npc in self.npcs)
        num_total = len(self.npcs)
        return 1 + (num_converted / num_total)


class Neighborhood:
    """
    This class represents a neighborhood that the player can visit. A neighborhood 
    has a number of locations.
    """
    def __init__(self, num_locations):
        self.locations = [Location(random.randint(0, 10)) for _ in range(num_locations)]


class Game:
    """
    This class represents the game itself. The game has a score, representing the total 
    number of NPCs converted, and a hunger level, which increases as the player takes actions. 
    When the hunger level reaches 100, the day ends and the player must rest. The game also 
    keeps track of the player's chosen religion, the conversion rate for each religion, and 
    the neighborhoods that the player can visit.
    """
    def __init__(self):
        self.score = 0
        self.satanic_score = 0
        self.hunger = 0
        self.revisit_list = []
        self.religions = ['Evangelist', 'Jehovah\'s Witness', 'Mormon', 'Custom']
        self.conversion_rates = {'Evangelist': 0.3, 'Jehovah\'s Witness': 0.2, 'Mormon': 0.25, 'Custom': 0.15, 'Satanic': 0.5}
        self.neighborhoods = [Neighborhood(random.randint(1, 10)) for _ in range(2)]
        self.chosen_location = None
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.day_of_week = 0
        self.daily_score = 0

    def start_game(self):
        """
        This method starts the game. It welcomes the player, lets them choose a religion, 
        and then loops through each day of a week. Each day, the player goes door-to-door 
        trying to convert NPCs until their hunger level reaches 100. At the end of the week, 
        the game ends.
        """
        print("Welcome to Belen Torres Preaching The Truth\n")
        print("In this game, you play as a preacher for a chosen religion. Your goal is to win as many souls as you can by going door-to-door and preaching your faith. Your performance is scored based on the number of souls won.\n")
        print("Each day you will encounter various responses from people behind the doors, and your hunger will increase as you continue preaching. When your hunger reaches 100, the day ends and you must go home to rest.\n")
        print("Now, let's begin. Choose your religion...\n")
        self.choose_religion()
        for _ in range(7):
            self.new_day()
            while self.hunger < 100:
                self.door_to_door()
            self.hunger = 0
            self.day_of_week = (self.day_of_week + 1) % 7
            self.daily_score = 0
        self.end_game()

    def choose_religion(self):
        """
        This method allows the player to choose their religion from a list of options.
        """
        print("Choose your religion:\n")
        for i, religion in enumerate(self.religions, start=1):
            print(f"{i}. {religion}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(self.religions):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.religions)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.religion = self.religions[choice - 1]
        print(f"You've chosen: {self.religion}\n")

    def new_day(self):
        """
        This method starts a new day in the game. It randomly sets the weather, 
        and then lets the player choose a neighborhood and location to visit.
        """
        self.weather = random.choice(['hot', 'cold', 'nice'])
        print(f"A new day begins... The weather is {self.weather}.")
        self.choose_neighborhood_and_location()

    def choose_neighborhood_and_location(self):
        """
        This method lets the player choose a neighborhood and location to visit 
        from a list of options.
        """
        print("Choose your neighborhood:\n")
        for i, neighborhood in enumerate(self.neighborhoods, start=1):
            print(f"{i}. Neighborhood {i} with {len(neighborhood.locations)} locations")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(self.neighborhoods):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.neighborhoods)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        chosen_neighborhood = self.neighborhoods[choice - 1]
        print(f"You've chosen: Neighborhood {choice}\n")

        print("Choose your location:\n")
        for i, location in enumerate(chosen_neighborhood.locations, start=1):
            print(f"{i}. Location {i} with {len(location.npcs)} NPCs")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(chosen_neighborhood.locations):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(chosen_neighborhood.locations)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.chosen_location = chosen_neighborhood.locations[choice - 1]
        print(f"You've chosen: Location {choice}\n")

    def door_to_door(self):
        """
        This method represents the player going door-to-door to try to convert NPCs. 
        It loops until the player's hunger level reaches 100. On each iteration, the 
        player chooses an NPC to approach, chooses a preaching strategy, and then 
        has an encounter with the NPC.
        """
        while self.hunger < 100:
            self.clear_console()
            print(f"You are at a {self.chosen_location.type} with {len(self.chosen_location.npcs)} people.\n")
            for i in range(len(self.chosen_location.npcs)):
                npc_status = "Converted" if self.chosen_location.npcs[i].converted else "Not Converted"
                print(f"{i + 1}. Person {i + 1}: {npc_status}")
            print("Choose a person to approach or enter 0 to move on.")
            while True:
                try:
                    choice = int(input("Enter the number of your choice: "))
                    if 0 <= choice <= len(self.chosen_location.npcs):
                        break
                    else:
                        print(f"Invalid choice. Please enter a number between 0 and {len(self.chosen_location.npcs)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            if choice == 0:
                print("Moving on to the next location...\n")
                self.choose_neighborhood_and_location()
                continue
            chosen_npc_id = choice - 1
            if self.chosen_location.npcs[chosen_npc_id].converted:
                print("This person has already been converted.\n")
                continue
            print("Approaching the chosen person...\n")
            self.choose_strategy()
            self.encounter(chosen_npc_id)
            self.hunger_increase()
            next_action = input("Press Enter to continue, or 'd' to view the dashboard.")
            if next_action.lower() == 'd':
                self.display_dashboard()

    def hunger_increase(self):
        """
        This method increases the player's hunger level based on the weather. If 
        the weather is hot or cold, the hunger level increases by 15; otherwise, 
        it increases by 10. If the hunger level reaches 100, the player is informed 
        that they are too hungry to continue and must go home to rest.
        """
        if self.weather == 'hot' or self.weather == 'cold':
            self.hunger += 15
        else:
            self.hunger += 10
        print(f"Your hunger level is now {self.hunger}.")
        if self.hunger >= 100:
            print("You're too hungry to continue. Time to go home and rest.")

    def choose_strategy(self):
        """
        This method lets the player choose a preaching strategy from a list of options.
        """
        print("Choose your preaching strategy:\n")
        strategies = ['Preach Softly', 'Preach Intensely']
        for i, strategy in enumerate(strategies, start=1):
            print(f"{i}. {strategy}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(strategies):
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(strategies)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.strategy = strategies[choice - 1]
        print(f"You've chosen to: {self.strategy}\n")

    def encounter(self, npc_id):
        """
        This method represents an encounter between the player and an NPC. If the NPC 
        is resistant, the encounter ends. Otherwise, the conversion rate is adjusted 
        based on the proportion of NPCs at the location that have been converted, and 
        then the NPC has a chance to respond positively or negatively to the player's 
        preaching. If the NPC responds positively, there is a chance that they will be 
        converted. If the NPC is converted, the player's score increases, and there is 
        a chance that the NPC will donate food to the player.
        """
        chosen_npc = self.chosen_location.npcs[npc_id]
        if chosen_npc.resistant:
            print("This person is resistant to conversion.")
            return
        conversion_rate_multiplier = self.chosen_location.get_conversion_rate_multiplier()
        for religion in self.conversion_rates:
            self.conversion_rates[religion] *= conversion_rate_multiplier
        conversion_rate = max(0, self.conversion_rates[self.religion] - chosen_npc.failed_attempts * 0.1)
        responses = ['bad', 'nice']
        response = random.choices(
            responses,
            weights=[1 - conversion_rate, conversion_rate],
            k=1
        )[0]
        if response == 'bad':
            print("The person is not interested.")
            self.bad_response()
            chosen_npc.failed_attempts += 1
        elif response == 'nice':
            print("The person is interested.")
            chosen_npc.convert(self.religion, conversion_rate)
            if chosen_npc.converted:
                print("The person converts!")
                if self.religion == 'Satanic':
                    self.satanic_score += 1
                else:
                    self.score += 1
                    self.daily_score += 1
                if random.random() < 0.2:
                    self.food_donation()

    def food_donation(self):
        """
        This method represents the player receiving a food donation from an NPC. 
        The player can choose to eat the food immediately, which reduces their 
        hunger level by 20.
        """
        print("The person donates some food to you!\n")
        eat_food = input("Do you want to eat the donated food now? (y/n) ")
        if eat_food.lower() == 'y':
            print("You eat the food and feel less hungry.\n")
            self.hunger = max(0, self.hunger - 20)

    def bad_response(self):
        """
        This method represents the player receiving a bad response from an NPC. 
        There is a chance that the NPC will throw a Satanic Bible at the player, 
        which gives the player the option to become a Satanic preacher. There is 
        also a chance that the player will meet another Satanic preacher, who will 
        join their cause and double the conversion rate for Satanism.
        """
        if random.random() < 0.1:
            if random.random() < 0.5:
                self.food_donation()
            elif self.religion != 'Satanic':
                self.receive_satanic_bible()
            else:
                self.meet_satanic_preacher()

    def receive_satanic_bible(self):
        """
        This method represents the player receiving a Satanic Bible from an NPC. 
        The player can choose to take the Bible and become a Satanic preacher.
        """
        print("The person throws a Satanic Bible at you!")
        take_bible = input("Do you want to take the Satanic Bible and become a Satanic preacher? (y/n) ")
        if take_bible.lower() == 'y':
            print("You take the Satanic Bible and become a Satanic preacher!")
            self.religion = 'Satanic'

    def meet_satanic_preacher(self):
        """
        This method represents the player meeting another Satanic preacher. The 
        other preacher joins the player's cause, and the conversion rate for 
        Satanism is doubled.
        """
        print("You meet another Satanic preacher who joins your cause!")
        self.conversion_rates['Satanic'] *= 2

    def end_game(self):
        """
        This method ends the game. If the player has converted at least three 
        locations into churches, they win the game. Otherwise, the game ends with 
        a message displaying the total number of souls won. If the player has won 
        at least 10 souls to Satanism, they have the option to become a vampire or 
        a werewolf.
        """
        num_churches = sum(location.church for neighborhood in self.neighborhoods for location in neighborhood.locations)
        if num_churches >= 3:
            print("You've created three churches and won the game!")
        else:
            print(f"You've won {self.score} souls!")
        if self.satanic_score >= 10:
            self.become_supernatural()

    def become_supernatural(self):
        """
        This method represents the player becoming a supernatural creature. The 
        player can choose to become a vampire or a werewolf.
        """
        while True:
            choice = input("You've won 10 souls to Satanism! Would you like to become a vampire or a werewolf? (v/w) ")
            if choice.lower() in ['v', 'w']:
                break
            else:
                print("Invalid input. Please enter 'v' for vampire or 'w' for werewolf.")
        if choice.lower() == 'v':
            print("You become a vampire and win the game!")
        else:
            print("You become a werewolf and win the game!")

    def clear_console(self):
        """
        This method clears the console. It checks the operating system and uses 
        the appropriate command to clear the console.
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_dashboard(self):
        """
        This method displays the game's dashboard, which includes the current day 
        of the week, the total number of people converted, the number of people 
        converted that day, the player's hunger level, and the weather.
        """
        self.clear_console()
        print(f"Day of the week: {self.days[self.day_of_week]}")
        print(f"Total people converted: {self.score}")
        print(f"People converted today: {self.daily_score}")
        if self.religion == 'Satanic':
            print(f"People converted to Satanism: {self.satanic_score}")
        print(f"Hunger level: {self.hunger}")
        print(f"Weather: {self.weather}")
        input("\nPress Enter to continue...")

game = Game()
game.start_game()
