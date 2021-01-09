# Tikademy

#### Video Demo: https://youtu.be/8P5XgSBqOVU

#### Description:

Hi, and welcome to Tikademy!

Tikademy is a matching website that connects tutors and students based on grade level, subject, and schedules. Anyone can sign up and once they submit their perferences, they will
be matched to another person who has complementary availabilities. Once you make an account, you can submit a form as a student or as a tutor (or both, if you are good in one subject but need
help in another). If you need to resubmit the form because of schedule changes, feel free to do so and the information will updated immediately! Once you've submitted the information, go to
the match page, where you just check off which you want to get matched to (in case you submitted both a tutor and student form) and you will recieve your matches! Note that once you get matches,
you can't get other matches. On that match page, you recieve the first name and email of all the people who you match with.

Good luck and I hope you enjoy it!

#### Files:

In the static folder is all the png files I used for images. These aren't really important for the code, but rather, they help improve the visuals. Also, the styles.css iles
is in here, so all the style info comes from this file.

In the templates folder I have all the HTML files. layout.html is the layout and all the other files are extensions of this. Apology is the same as 2020's CS50 finance web app.

Finally, not in any folder, we have application.py, which is the main Python/Flask document that is running all the web appy stuff. This is the file that runs. We also have helpers.py,
which has a few helper functions for things like apology pages. Also included is app.py, which is a previously working piece of code. It's currently useless though, but it's nice to
have as a last checkpoint before the completed version. Finally, other than this README file, we have project.db, which is the database that stores all the information that is being
collected and used by the webapp.

#### Design Choices:

This is probably not the best designed web app but I started it in the summer and I couldn't finish before my first semester of college started and so I somewhat forgot about all the
variables and things I had been working on when I finished it this Decemeber/January. One major design choice I had was to let one person account be able to have a tutor and student account
in case people needs help in both. I also think the database is poorly designed, so instead of a wide table, I should have had a tall one. But I had already created the table and
wrote out wayyyyyy too many repetitive lines of code. Going forward, I will never do this again because I've learned my lesson.

#### Final Thoughts:

I've learned a lot about how hard it is to come up with an idea and create something out of it. I think my idea is actually really good because it's something that I noticed and was
frustrated with in high school. As a part of National Honor Society, there was a disconnect between kids who wanted tutors and older students who needed volunteer hours. I tried to
address that issue with Tikademy. And althought it is very "janky" in nature, it does the job. I wish I had done a better job of thinking out all the features before writing the code
because that would have lead to overall better design in the webapp and database. I think looking at the Flask documentation would have helped me with figuring out better ways to
do the things I wanted to do, rather than finding ways to circumvent the topic. Overall though, this was a great learning experience and I will come out of this final project a lot
smarter and a lot more aware of what it means to build a project from start to finish!