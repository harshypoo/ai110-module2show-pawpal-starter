# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. 
This design handles the pet owner, pet, tasks, and daily schedule. It has all the methods that
a pet owner would require to handle the daily tasks for a pet. It describes the function of the app
in one diagram.
- What classes did you include, and what responsibilities did you assign to each?
I included the Pet, Owner, Task, and Scheduler classes. Scheduler makes a schedule for the tasks,
Owner is the owner of the pet, Pet is the animal, and Task is a task for the pet.

**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
I changed the daily time budget, Owner.available_minutes, because it only accounts for one pet. If there are
multiple pets, then the daily time budget is split across all of those pets. It conflicts with the pet(s) 
requirements. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler uses exact time matching depending on the day and HH:MM format. This does not account
for how long a task may take to complete, and if it overlaps with the next task.
- Why is that tradeoff reasonable for this scenario?
We are just looking for a schedule creator, not a way to track how long we take with a specific
task and what is next.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to brainstorm the UML design and understand what we would need to make this app completely cohesive.
I then asked it to implement logic and brainstormed with it more to understand what other features we could
add to future-proof this app.
- What kinds of prompts or questions were most helpful?
The prompts where I was conversing back and forth and getting an understanding of the system design was
very helpful. The implementation was a plus, but the design matters more.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
The AI was trying to assign different names for a class, but I wanted to keep it simple and not make
developers confused when reading the code, so I kept it simple and did not use multiple names for one class.
- How did you evaluate or verify what the AI suggested?
I used the tests provided by the AI and also referred to the UML to ensure that all of the classes are
cohesive and line up with what we are trying to accomplish with this app.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the sorting functionality, recurring tasks creating new instances as needed, duplicates being
found, invalid inputs being handled, and more. There were happy and edge cases.
- Why were these tests important?
We need to think like a human and find ways that they would unintentionally break the code to see 
how we can fix it right now and future-proof it. We also need to make sure that the correct
features are actually working.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am 4/5 stars confident that the scheduler works correctly now. AI can never be 100% confident,
but I am more confident with my understanding of the code and tests.
- What edge cases would you test next if you had more time?
I would test for many owners, many pets, and many tasks. We want to make sure that the data is being
associated with the correct objects, not being jumbled all over the place.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am very satisfied with how I was able to build an app and brainstorm with AI to create the design.
The UML was the most helpful part because it explained the entirety of the app, and AI helped a lot with that.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would add more features that can really future-proof this app. The task ID was the AI's addition, which
was really smart and helpful. I would add more features to make this app really unique and maybe even add
a community schedule so that other members can view the schedules of different pets and owners.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
You have to have a strong understanding of what you are building, through a UML, before you start building.
If you are unsure of the relationships between different classes and the entire outcome of the project,
then you are not going to have a good time. You need to understand what you are building before you start
writing code!