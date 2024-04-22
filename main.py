from psychopy import visual, core, gui
from psychopy.visual.circle import Circle
from psychopy.hardware import keyboard
import random
import csv

# Define parameters
num_trials = 2
blink_duration = 0.075  # in milliseconds
one_lett_duration = 0.015  # duration of displaying one letter
fixation_duration = 0.018  # duration of displaying fixation point
num_post_targ = 3  # number of target letters after white letter
num_post_non_targ = 5  # number of letters after all target letters
num_post = num_post_targ + num_post_non_targ  # number of all post white-letter target
height_stim = 70  # size of letters
height_text = 40  # size of text
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W",
           "X", "Y", "Z"]

user_answers = []  # list of answers ['Subject_index', 'Target_index', 'Is_correct']

# initialization of user keyboard
keyboard = keyboard.Keyboard()


def ini_win():
    win = visual.Window([1280, 720], color="gray", units="pix", fullscr=True)
    return win


# initialize all text screens and stimuli (WITHOUT WINDOW)
def ini_stims(window):
    # Define fixation point
    fixation = Circle(window, radius=5, color="white")

    # instruction before trials
    instruction_text = visual.TextStim(win=window, name='instruction_text',
                                       text='Skup się na literze białej i trzech literach po literze białej, postaraj się je wszystkie zapamiętać. Na końcu zostaniesz poproszony o naciśnięcie po kolei 4 klawiszy z literami, które zaobserwowałeś.\nKiedy będziesz gotowy naciśnij klawisz SPACJA',
                                       font='Open Sans',
                                       height=height_text)

    # blank text
    blank_text = visual.TextStim(win=window, name='blank_text',
                                 text=None,
                                 font='Open Sans',
                                 pos=(0, 0), height=height_stim, wrapWidth=None, ori=0.0,
                                 color='white', colorSpace='rgb', opacity=None,
                                 languageStyle='LTR',
                                 depth=0.0);

    answer_white_target = visual.TextStim(win=window, name='Intruction_for_answer',
                                          text='Jaka litera pojawiła się jako litera biała?\nNaciśnij klawisz odpowiadający literze, którą widziałeś/widziałaś.\nUWAGA - klawisz możesz nacisnąć tylko raz, potem nie będzie powrotu!',
                                          font='Open Sans',
                                          pos=(0, 0), height=height_text, wrapWidth=None, ori=0.0,
                                          color='white', colorSpace='rgb', opacity=None,
                                          languageStyle='LTR',
                                          depth=0.0);

    answer_target1 = visual.TextStim(win=window, name='Intruction_for_answer1',
                                     text='Jaka litera pojawiła się OD RAZU PO literze białej?\nNaciśnij klawisz odpowiadający literze, którą widziałeś/widziałaś.\nUWAGA - klawisz możesz nacisnąć tylko raz, nie ma możliwości powrotu!',
                                     font='Open Sans',
                                     pos=(0, 0), height=height_text, wrapWidth=None, ori=0.0,
                                     color='white', colorSpace='rgb', opacity=None,
                                     languageStyle='LTR',
                                     depth=0.0);

    answer_target2 = visual.TextStim(win=window, name='Instruction_for_answer2',
                                     text='Jaka litera pojawiła się jako kolejna? Druga litera po literze białej.\nNaciśnij klawisz odpowiadający literze, którą widziałeś/widziałaś.\nUWAGA - klawisz możesz nacisnąć tylko raz, potem nie będzie powrotu!',
                                     font='Open Sans',
                                     pos=(0, 0), height=height_text, wrapWidth=None, ori=0.0,
                                     color='white', colorSpace='rgb', opacity=None,
                                     languageStyle='LTR',
                                     depth=0.0);

    # --- Initialize components for Routine "Answer_three" ---
    answer_target3 = visual.TextStim(win=window, name='Instruction_for_answer3',
                                     text='Jaka litera pojawiła się jako kolejna? Trzecia litera po literze białej.\nNaciśnij klawisz odpowiadający literze, którą widziałeś/widziałaś.\nUWAGA - klawisz możesz nacisnąć tylko raz, potem nie będzie powrotu!',
                                     font='Open Sans',
                                     pos=(0, 0), height=height_text, wrapWidth=None, ori=0.0,
                                     color='white', colorSpace='rgb', opacity=None,
                                     languageStyle='LTR',
                                     depth=0.0);

    return fixation, instruction_text, blank_text, answer_white_target, answer_target1, answer_target2, answer_target3


def ini_start_end_text(window):
    # Initialize welcome message screen
    welcome_message = visual.TextStim(win=window, name='welcome_message',
                                      text='Dzień dobry. Jesteśmy studentami Kognitywistyki na drugim roku. Bierze Pan/Pani udział w eksperymencie prowadzonym przez nas w ramach zaliczenia przedmiotu. Udział w eksperymencie jest dobrowolny i może zostać przez Panią/Pana przerwany w dowolnym momencie. \n\nNaciśnij klawisz SPACJA aby zacząć',
                                      font='Open Sans',
                                      height=height_text)

    # --- Initialize components for Routine "Goodbye_Screen" ---
    goodbye_message = visual.TextStim(win=window, name='goodbye_message',
                                      text='Dziękujemy za udział w badaniu!\nW razie wątpliwości lub pytań zapraszamy do kontaktu mailowego:\nlukasz.pawlik@student.uj.edu.pl\nAby wyjść naciśnij dowolny klawisz',
                                      font='Open Sans',
                                      pos=(0, 0), height=height_text, wrapWidth=None, ori=0.0,
                                      color='white', colorSpace='rgb', opacity=None,
                                      languageStyle='LTR',
                                      depth=0.0)

    return welcome_message, goodbye_message


def blank(window, blank_text):
    blank_text.draw()
    window.flip()
    core.wait(blink_duration)


#
def draw_letter(window, blank_text, text_stim, text_index):
    text_stim[text_index].draw()
    window.flip()
    core.wait(one_lett_duration)
    blank(window=window, blank_text=blank_text)


def quit_on_esc():
    if 'escape' in keyboard.waitKeys():
        core.quit()


# wait for keypress and save user answer
def answer_target(window, sub_index, text_stim, target_letts, post_letts, lett_index):
    text_stim.draw()
    window.flip()
    key_list = keyboard.waitKeys(keyList=None, waitRelease=True)
    # print(key_list[0].name)
    # print(post_letts)

    # check if user clicked correct letter
    if target_letts[lett_index] in key_list:
        user_answers.append([sub_index, lett_index, "Yes", "Yes", lett_index])
    # if not, check if pressed key is in post-target letters
    elif key_list[0].name in post_letts:
        user_answers.append([sub_index, lett_index, "No", "Yes", post_letts.index(key_list[0].name)])
    # check if user wants to quit
    elif 'escape' in key_list:
        window.close()
    # if not, then append with NaN
    else:
        user_answers.append([sub_index, lett_index, "No", "No", "No"])


def save_to_csv(correct_answers):
    with open('answers.csv', 'w', newline='') as csvfile:
        # If Target_index = 0 then it is white letter target
        fieldnames = ['Subject_index', 'Target_index', 'Is_correct', 'Is_in_posts', 'Post_index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for lst in correct_answers:
            writer.writerow(
                {'Subject_index': lst[0], 'Target_index': lst[1], 'Is_correct': lst[2], 'Is_in_posts': lst[3],
                 'Post_index': lst[4]})


def open_dlg():
    sub_dict = {
        'sub_index': "Napisz tu swój numer badanego"
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=sub_dict, sortKeys=False, title='expName', show=True, screen=-1)
    if not dlg.OK:
        core.quit()  # user pressed cancel
    participant_num = dlg.data["sub_index"]

    return participant_num


def make_trials(window, participant_num):
    fixation, instruction_text, blank_text, answer_white_target, answer_target1, answer_target2, answer_target3, = ini_stims(
        window=window)
    for n in range(num_trials):
        random.shuffle(letters)  # shuffle letters on each trial
        num_letts = random.randint(7, 15)  # random number of pre-target letters
        index_after_white = num_letts + 1  # index of first post-white letter target
        end_targets = index_after_white + 3  # index when targets will end
        # make list of only target letters (white target - post - post - post)
        target_letts = [letter.lower() for letter in letters[num_letts:end_targets]]
        # make list with all post-target letters
        post_letts = [letter.lower() for letter in letters[num_letts:index_after_white + num_post]]

        # initialize all letters as stimuli
        trial_letters = [visual.TextStim(win=window, name='rand_letter',
                                         text=number,
                                         font='Open Sans',
                                         pos=(0, 0), height=height_stim, wrapWidth=None, ori=0.0,
                                         color='black', colorSpace='rgb', opacity=1.0,
                                         languageStyle='LTR',
                                         depth=0.0) for number in letters]

        # initialize white target letter as stimuli
        white_target = visual.TextStim(win=window, name='rand_letter',
                                       text=letters[num_letts],
                                       font='Open Sans',
                                       pos=(0, 0), height=height_stim, wrapWidth=None, ori=0.0,
                                       color='white', colorSpace='rgb', opacity=1.0,
                                       languageStyle='LTR',
                                       depth=0.0)

        # draw instruction on screen
        instruction_text.draw()
        window.flip()
        quit_on_esc()

        # draw fixation point on screen
        fixation.draw()
        window.flip()
        core.wait(fixation_duration)

        # draw all non-target letters with blank on screen
        for i in range(num_letts):
            draw_letter(window=window, blank_text=blank_text, text_stim=trial_letters, text_index=i)

        # draw white target letter on screen
        white_target.draw()
        window.flip()
        core.wait(one_lett_duration)
        blank(window=window, blank_text=blank_text)

        # draw targets after white letter
        for i in range(index_after_white, index_after_white + num_post_targ):
            draw_letter(window=window, blank_text=blank_text, text_stim=trial_letters, text_index=i)
        # draw post-target letters
        start_post_non_targ = index_after_white + num_post_targ + 1
        end_post_non_targ = start_post_non_targ + num_post_non_targ
        for i in range(start_post_non_targ, end_post_non_targ):
            draw_letter(window=window, blank_text=blank_text, text_stim=trial_letters, text_index=i)

        # ask for white target letter
        answer_target(window=window, sub_index=participant_num, text_stim=answer_white_target,
                      target_letts=target_letts, post_letts=post_letts, lett_index=0)
        # ask for first post-target
        answer_target(window=window, sub_index=participant_num, text_stim=answer_target1,
                      target_letts=target_letts,
                      post_letts=post_letts,
                      lett_index=1)
        # ask for second post-target
        answer_target(window=window, sub_index=participant_num, text_stim=answer_target2,
                      target_letts=target_letts,
                      post_letts=post_letts,
                      lett_index=2)
        # ask for third post-target
        answer_target(window=window, sub_index=participant_num, text_stim=answer_target3,
                      target_letts=target_letts,
                      post_letts=post_letts,
                      lett_index=3)


if __name__ == "__main__":
    # make dialog for input participant number
    part_index = open_dlg()

    # initialize window
    win = ini_win()
    # initialize welcome and goodbye message
    welcome_message, goodbye_message = ini_start_end_text(window=win)

    # draw welcome screen with introduction
    welcome_message.draw()
    win.flip()
    # check if user wants to exit
    quit_on_esc()

    # make all trials, appending "answers" list with correct answers
    make_trials(window=win, participant_num=part_index)

    # draw goodbye screen
    goodbye_message.draw()
    win.flip()
    # check if user wants to exit
    quit_on_esc()

    # save data to csv
    save_to_csv(user_answers)
