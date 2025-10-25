""" 
This file (kbc_module.py) contains question and KBCGame classes
and their helper functions. It is done to separate the
game logic from the main running file. 
Demonstrates : Modularization.
"""
import csv
import random
from datetime import datetime
from typing import List

class Question:
    """
    Question class stores info about one single qn.
    Demonstrates : OOPs, Classes and objects, instance variable
    and methods.
    By convention we use a leading underscore for 'private'
    (access modifier style)
    """
    def __init__(self, qid, category, text, options, answer):
        """
        qid : string/int id of the question.
        category : category of the qn - hard/harder/hardest
        text : question text (string)
        options : tuple/list of 4 option strings.
        answer : a/b/c/d (string)
        """
        self.qid=qid
        self.category=category
        self.text=text
        self.options=tuple(options)
        self.answer=answer.lower()

    def display(self):
        # simple display helpr function.
        print(self.text)
        labels=["a","b","c","d"]
        for lab,opt in zip(labels, self.options):
            print(f"{lab}) {opt}")
    
class KBCGame:
    """Encapsulates game logic and player state."""

    def __init__(self, questions: List[Question]):
        self._questions_bank=list(questions) #private-convention
        self._prizes=[0,1000,2000,5000,10000,25000,50000,
                      100000,200000,500000,1000000]
        self._checkpoints={4:10000,7:100000,10:10000000}
        self.reset_game_state()
    
    def reset_game_state(self):
        self.current_winnings=0
        self.current_qno=0
        self.asked_questions: List[Question]=[]
        self.player_name=""
    
    def select_questions_for_game(self):
        """Pick 3 hard, 3 harder, 4 hardest questions randomly."""
        cat_map={'hard':[],'harder':[],'hardest':[]}
        for q in self._questions_bank:
            if q.category in cat_map:
                cat_map[q.category].append(q)
        required={'hard':3, 'harder':3, 'hardest':4}
        for cat,req in required_items():
            if len(cat_map[cat])<req:
                raise ValueError(f"Not enough {cat} questions (need {req}).")
            
        selected=[]
        selected+=random.sample(cat_map['hard'],3)
        selected+=random.sample(cat_map['harder'],3)
        selected+=random.sample(cat_map['hardest'],4)
        self.asked_questions=selected
        return selected
    
    def get_prize_for_qno(self,qno:int)->int:
        return self._prizes[qno] if 0<=qno<len(self._prizes) else 0
    
    def is_checkpoint(self,qno:int)->bool:
        return qno in self._checkpoints
    
    def last_passed_checkpoint_amount(self, last_qno:int)->int:
        """Return the value of the last passed checkpoint."""
        passed=0
        for cp in sorted(self._checkpoints.keys()):
            if last_qno>=cp:
                passed=self._checkpoints[cp]
        return passed
    
    def ask_question(self, qno:int, qobj:Question):
        """Ask one question, validate input, return (correct, quit_flag)."""
        print(f"\nQuestion {qno} for ₹{self.get_prize_for_qno(qno)}")
        qobj.display()
        
        while True:
            ans=input("Enter your answer (a/b/c/d): ").strip().lower()
            if ans in ('a','b','c','d'):
                return ans==qobj.answer,False
            print("Invalid input. Please enter only a/b/c/d).")
        
    @staticmethod
    def save_score_to_csv(player_name:str,winnings:int,filename='scores.csv'):
        """Append score with header if file is new."""
        now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header=['player_name','winnings','timestamp']
        try:
            need_header=not os.path.exists(filename)
        except Exception:
            need_header=True
        try:
            with open(filename,'a',newline='',encoding='utf-8') as f:
                writer=csv.writer(f)
                if need_header:
                    writer.writerow(header)
                writer.writerow([player_name,winnings,now])
        except Exception as e:
            print(f"Error saving score: {e}")
            
    def load_questions_from_csv(csv_filename='questions.csv')->List[Question]:
        """Load questions from CSV (id,category,question,a,b,c,d,answer)."""
        questions:List[Question]=[]
        try:
            with open(csv_filename,'r',encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    try:
                        q=Question(
                            row['id'],row['category'],row['question'],
                            [row['a'],row['b'],row['c'],row['d']],row['answer']
                        )
                        questions.append(q)
                    except Exception:
                        continue
        except FileNotFoundError:
            print(f"File {csv_filename} not found.")
        return questions
