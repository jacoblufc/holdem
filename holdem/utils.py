# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Sam Wenke (samwenke@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from treys import Card, Evaluator
import random, numpy as np
#import holdem_calc
Eval = Evaluator()
class action_table:
  CHECK = 0
  CALL = 1
  RAISE = 2
  FOLD = 3
  NA = 0


def format_action(player, action):
  color = False
  try:
    from termcolor import colored
    # for mac, linux: http://pypi.python.org/pypi/termcolor
    # can use for windows: http://pypi.python.org/pypi/colorama
    color = True
  except ImportError:
    pass
  [aid, raise_amt] = action
  if aid == action_table.CHECK:
    text = '_ check'
    if color:
      text = colored(text, 'white')
    return text
  if aid == action_table.CALL:
    text = '- call, current bet: {}'.format(player.currentbet)
    if color:
      text = colored(text, 'yellow')
    return text
  if aid == action_table.RAISE:
    text = '^ raise, current bet: {}'.format(raise_amt)
    if color:
      text = colored(text, 'green')
    return text
  if aid == action_table.FOLD:
    text = 'x fold'
    if color:
      text = colored(text, 'red')
    return text


def card_to_str(card):
  if card == -1:
    return ''
  return Card.int_to_pretty_str(card)


def hand_to_str(hand):
  output = " "
  for i in range(len(hand)):
    c = hand[i]
    if c == -1:
      if i != len(hand) - 1:
        output += '[  ],'
      else:
        output += '[  ] '
      continue
    if i != len(hand) - 1:
      output += str(Card.int_to_pretty_str(c)) + ','
    else:
      output += str(Card.int_to_pretty_str(c)) + ' '
  return output


def safe_actions(community_infos, n_seats):
  current_player = community_infos[-1]
  to_call = community_infos[-2]
  actions = [[action_table.CHECK, action_table.NA]] * n_seats
  if to_call > 0:
    actions[current_player] = [action_table.CALL, action_table.NA]
  return actions


def random_acts(com_infos, seats):
    to_call = com_infos[-2]
    actions = []
    for player in range(seats):
        temp_act = get_rand_action(to_call)
        # print(player, temp_act)
        actions.append(temp_act)
    return actions


def get_rand_action(to_call):
    # print("Here")
    #rand_act = [0, 0]
    if to_call > 0: #if we need to call
      # if random.uniform(0, 1) < Epsilon:
      Call_Fold = random.uniform(0, 1) #In this situ we can either call or fold
      if Call_Fold <= 0.5:
        #print("Fold")
        rand_act = [3, 0] #Fold
      else:
        #print("Call")
        rand_act = [1, 0] #Call
    else:
      Check_Raise = random.uniform(0, 1)
      if Check_Raise <= 0.5:
        # print("Check")
        rand_act = [0, 0] #Check
      else:
        # print("Raise")
        rand_act = [2, 25] #Raise, note the min raise of the game is 25
    return rand_act


def rand_actions(community_infos, n_seats, actions):
    current_player = community_infos[-1]
    to_call = community_infos[-2]
    #actions = [[action_table.CHECK, action_table.NA]] * n_seats
    if current_player==0:
      if to_call > 0:
          #print("Player", current_player, "To call yes", to_call)
          Call_Fold = random.randint(0, 1) #In this situ we can either call or fold
          if Call_Fold == 0:
            #print("Fold")
            actions[current_player] = [3, 0] #Fold
          else:
            #print("Call")
            actions[current_player] = [1, 0] #Call
      else:
      # print("Player", current_player, "To call no", to_call)
        Check_Raise = random.randint(0, 1)
        if Check_Raise == 0:
          # print("Check")
          actions[current_player] = [0, 0] #Check
        if Check_Raise == 1:
          # print("Raise")
          actions[current_player] = [2, 50] #Raise, note the min raise of the game is 25
    return actions


def inserted_actions(actions):

    # get user to input raise aswell if user_input=2
    user_input = None
    while user_input is None:
      print ("Choose action by number")
      key=input()
      try:
        user_input=int(key)
      
      except ValueError or AssertionError:
        print ("try again") 
        pass
    #actions[2]=[user_input,0]
    return actions


def probabilistic_actions(community_infos, player_infos, n_seats):
    # makes every other player
    current_player = community_infos[-1]
    to_call = community_infos[-2]
    approx_prob=(1-((player_infos[current_player][4])/7462))
    # print(approx_prob)
    # bypasses preflop, by just calling or checking
    # Need to bin preflop cards into q_state rank
    actions = [[action_table.CHECK, action_table.NA]] * n_seats
    if approx_prob > 1:
      if to_call > 0 :
        actions[current_player] = [1, 0] # call
      else:
        actions[current_player] = [0,0] # check
        

    elif to_call > 0:
      # put conditional so if > 0.9 raise the call
      if approx_prob > 0.3:
        actions[current_player] = [1, 0] #call
      else:
        actions[current_player] = [3, 0] #fold


    else:
    # print("Player", current_player, "To call no", to_call)
      if approx_prob > 0.6:
        actions[current_player] = [2, 25] #Raise, note the min raise of the game is 25
      else:
        actions[current_player] = [0, 0] # check
    
    return actions


def get_best_action(to_call, Q_state, Q_Table):
    check, call, rais, fold = Q_Table[Q_state]
    if to_call > 0:
        if call > fold:
            best_action = [1, 0]
        elif call < fold:
            best_action = [3, 0]
        else:
            best_action = get_rand_action(to_call)
    else:
        if check > rais:
            best_action = [0, 0]
        elif check < rais:
            best_action = [2, 25]
        else:
            best_action = get_rand_action(to_call)

    return best_action


def get_state(handrank):
    if handrank < 0:
        return -1
    elif handrank in range(1, 11):
        State = 0
    elif handrank in range(11, 167):
        State = 1
    elif handrank in range(167, 323):
        State = 2
    elif handrank in range(323, 1600):
        State = 3
    elif handrank in range(1600, 1610):
        State = 4
    elif handrank in range(1610, 2468):
        State = 5
    elif handrank in range(2468, 3326):
        State = 6
    elif handrank in range(3326, 6186):
        State = 7
    elif handrank in range(6186, 7463):
        State = 8
    return State


def eval_hand(hand, board):
    for card in range(len(board) - 1, -1, -1):  # iterate over reversed indices's
        if board[card] == -1:
            del board[card]
    Sol = Eval.evaluate(hand, board)
    return Sol


def prob_action(plrhand, tocall, river):
    # print("prob")
    rank = eval_hand(plrhand, river)
    approx_prob = 1 - rank/7462
    if tocall > 0:
        if approx_prob > 0.2:
            # print("call")
            return [1, 0] #call
        else:
            # print("fold")
            return [3, 0]#fold
    else:
        if approx_prob > 0.6:
            # print("raise")
            return [2, 25]#raise
        else:
            # print("check")
            return [0, 0]#check
