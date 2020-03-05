import requests
from bs4 import BeautifulSoup
from .exceptions import NotFoundException, ConnectionException
import re


class FriendResult:

    def __init__(self, url: str) -> None:
        self.url = url
        self.response = ''
        self.is_found = False

    def get_response(self) -> str:
        """
        This function gets the response of webpage
        """
        req = requests.get(self.url, headers={
                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'})
        if req.status_code == 200:
            if "Select Language" in req.text:
                raise NotFoundException("This id is not valid")
            else:
                self.response = req.text
                self.is_found = True
                return req.text

        else:
            return ConnectionException("There was a problem getting the info")

    def get_parser(self):
        """
        This function returns the beautifulsoup parser
        """
        try:
            self.get_response()
            return True, BeautifulSoup(self.response, 'html.parser')
        except NotFoundException:
            return False, None

    def get_answers(self) -> list:
        """
        This function returns the list of question with the correct answer

        question div class = question hidden unanswered
        questions text class = fivepxtop question_attempt_text
        """

        is_found, parser = self.get_parser()
        if is_found:
            answers = []
            questions_fields = parser.find_all(
                "div", {"class": "question hidden unanswered"})
            print(questions_fields)
            for question_fields in questions_fields:
                question = question_fields.find(
                    "h3", {"class": "fivepxtop question_attempt_text"}).get_text().strip()
                answer = question_fields.find(
                    "td", {"class": "answer center correct"}).get_text().strip()
                answers.append(dict(question=question, answer=answer))
            return answers
        else:
            return None

    def get_name(self) -> str:
        is_found, parser = self.get_parser()
        if is_found:
            name_txt = parser.find(
                "h3", {"class": "fivepxtop tenpxbottom center"}).get_text().strip()
            name = re.findall("How Well do you know (.+)?", name_txt)
            return name[0].replace("?", "")
        else:
            return None
