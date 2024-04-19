good_tasks = ["Take a walk", "Organize the shelf", "Read a book", "Talk on phone", "Take a nap", "Buy groceries", 
              "Clean out the trash", "Do the dishes", "Do the laundry", 
               "Take a bath", "Go to balcony"]

task_to_seq = {"Talk on phone": "phone", "Go to balcony": "balcony", "Clean out the trash":"trash", "Take a bath":"bath", 
               "Do the dishes":"sink", "Read a book":"book", 'Do the laundry':"wash", "Buy groceries":'door', 
               "Take a nap":"bed", "Take a walk":['tree1', 'tree2', 'tree3', 'tree4'], "Organize the shelf":"shelf"}

phone_codes = ["69420", "43210", "98543", "87658", "38961"]

task_to_points = {"Talk on phone": 15, "Go to balcony": 10, "Clean out the trash": 10, "Take a bath": 10, "Do the dishes": 15, 
                    "Read a book": 10, 'Do the laundry': 15, 'Buy groceries':10, "Take a nap": 10, 
                    'Take a walk':40, 'Organize the shelf':10}

bad_tasks = {1:["You browsed through social media for 2 hours.",  "Your mental health is reduced by 10 points."],
			2:["You ate a lot of junk food.", "Your mental health is reduced by 10 points."],
			3:["You watched TV for 3 hours", "Your mental health is reduced by 15 points"],
			4:["You overthought about your bad grade", "Your mental health is reduced by 15 points"],
			5: ["You stayed in bed all day and didn't talk to anyone", "Your mental health is reduced by 20 points"]}

happiness_reduced = {1:10, 2:10, 3:15, 4:15, 5:20}

task_to_obj = {"Talk on phone":'telephone', "Go to balcony":'chair', "Clean out the trash":'trashcan',
			    "Take a bath":'bathtub', "Do the dishes":'sink', "Read a book":'books',
				'Do the laundry':'washing_machine', "Buy groceries":'door', 'Take a nap':'bed',
				"Organize the shelf":'shelf', "Take a walk":['tree1', 'tree2', 'tree3', 'tree4']}

task_to_controls = {"Talk on phone":['Press "P" to open keypad/notes', 'Use number keys to type the code', 'Press "Enter" to enter the code', 'Use "Backspace"'],
					 "Go to balcony":['Hold "I" to relax'],
					 "Clean out the trash":['Hold "I" to clean out the trash'],
					 "Take a bath":['Hold "I" to take a bath'],
					 "Do the dishes":['Hold "I" to do the dishes'],
					 "Read a book":['Press "B" to open the book', "Use arrow keys to navigate", 'Use number keys to type the code', 'Press "Enter" to enter the code', 'Use "Backspace"'],
					 "Do the laundry":['Hold "I" to do the laundry'],
					 "Buy groceries":['Hold "I" to buy groceries'],
					 "Take a nap":['Hold "I" to take a nap'],
					 "Organize the shelf":['Hold "I" to organize the shelf'],
					 "Take a walk":['Hold "I" at each of the four trees']
					 }
index_to_name = {1419:'chair', 1389:'trashcan', 1357:'telephone', 1485:'bathtub', 1386:'sink', 1390:'books', 
				 1391:'notes', 1480:'washing_machine', 1742:'door', 1738:'bed', 1709:'shelf', 192:'tree1',
				 96:'tree2', 209:'tree3', 208:'tree4'}

difficulty_to_bad_task_wait = {'Easy':1500, 'Medium':1000, 'Hard':500}