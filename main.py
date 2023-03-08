import os
import numpy as np
import openai
import jellyfish

openai.api_key = os.environ['OPENAI_API_KEY']

recent_prompt = 'what should I do to get funding'
speakers = []
convo = []


def incoming_mms(actual_number):
  """Send a dynamic reply to an incoming text message"""
  global recent_prompt
  names = [
    'Elon Musk', 'Peter Thiel', 'Steve Jobs', 'Mark Cuban', 'Farza Majeed',
    'Naval Ravikant', 'Sam Altman'
  ]
  for i in range(actual_number):
    print('current_number : %s' % (i))
    response = board_of_advisors(names)
    print('jaro_distance is %s'%(jellyfish.jaro_distance(recent_prompt, response)))
    if jellyfish.jaro_distance(recent_prompt, response) < 0.7:
      convo.append(response)
      recent_prompt = response

    else:
      break


def board_of_advisors(names):
  global recent_prompt
  name = names[np.random.choice(len(names))]
  max_consecutive_messages = 3
  if speakers[-1 * max_consecutive_messages:].count(
      name) == max_consecutive_messages:
    print('speakers : %s : name : %s' % (speakers, name))
    not_this_person = name
    while name != not_this_person:
      name = names[np.random.choice(len(names))]
  s = ", "
  j = " "

  names_string = s.join(names)
  convo_string = j.join(convo)

  print('speakers : %s : name : %s' % (speakers, name))

  summary_prompt = """Summarize this text conversation between business leaders that are helping me get results: %s""" % (
    convo_string)
  #print('summary_prompt : %s' % (summary_prompt))
  convo_summary = openai.Completion.create(model="text-davinci-003",
                                           prompt=summary_prompt,
                                           temperature=0,
                                           max_tokens=64,
                                           top_p=1.0,
                                           frequency_penalty=0.0,
                                           presence_penalty=0.0)
  prompt = """ 
  The startup founders %s are having a long text conversation to exclusively answer my questions. This is the summary of the conversation %s. This is the last text %s. %s had a response, and they said:
    """ % (names_string, convo_summary, recent_prompt, name)

  #print('prompt : %s' % (prompt))

  response = openai.Completion.create(engine="text-davinci-003",
                                      prompt=prompt,
                                      temperature=0.7,
                                      max_tokens=256,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0)

  text = response['choices'][0]['text']

  recent_response = text.replace('"', '')
  speakers.append(name)

  print("""%s said %s""" % (name, recent_response))
  return recent_response


def run(number_of_messages):
  actual_number = np.random.choice(number_of_messages)
  actual_number = 10
  incoming_mms(actual_number)


run(10)
