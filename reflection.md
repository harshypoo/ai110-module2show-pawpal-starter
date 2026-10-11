# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. 
This design handles the pet owner, pet, tasks, and daily schedule. It has all the methods that
a pet owner would require to handle the daily tasks for a pet. It describes the function of the app
in one diagram.
- What classes did you include, and what responsibilities did you assign to each?
I included the Pet, PetOwner, CareTask, and Scheduler classes. Scheduler makes a schedule for the tasks,
PetOwner is the owner of the pet, Pet is the animal, and CareTask is a task for the pet.

**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
I changed the daily time budget, PetOwner.available_minutes, because it only accounts for one pet. If there are
multiple pets, then the daily time budget is split across all of those pets. It conflicts with the pet(s) 
requirements. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
