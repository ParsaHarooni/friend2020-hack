from friend2020.results import FriendResult

result = FriendResult("https://friend2020.com/quiz/25839172")
print("Answers:",result.get_answers())
print("Name:",result.get_name())
