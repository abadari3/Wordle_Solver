import urllib.request

allowed_words = urllib.request.urlopen("https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/de1df631b45492e0974f7affe266ec36fed736eb/wordle-allowed-guesses.txt").read().decode("utf-8").split("\n")
possible_words = urllib.request.urlopen("https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/5d752e5f0702da315298a6bb5a771586d6ff445c/wordle-answers-alphabetical.txt").read().decode("utf-8").split("\n")
possible_guesses = possible_words
hints = {
    "wrong":[],
    "present":[],
    "fixed":[]
}

def condition(w, hints):
    for fixed in hints["fixed"]:
        c, l = fixed
        if w[l] != c:
            return False
    for wrong in hints["wrong"]:
        if wrong in w:
            return False
    for var in hints["present"]:
        c, l = var
        if w[l] == c:
            return False
    return True

def gather_info():
    # best info gathering guess
    letters = {}
    for word in possible_guesses:
        for c in word:
            if c in letters:
                letters[c] += 1
            else:
                letters[c] = 1

    tried_chars = [x for x in hints["wrong"]]
    tried_chars.extend([x[0] for x in hints["fixed"]])
    tried_chars.extend([x[0] for x in hints["present"]])
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c in tried_chars:
                letters[c] = 0
        elif c not in letters:
            letters[c] = 0

    best_guess = ""
    max_score = 0
    for word in allowed_words:
        score = 0
        chars = []
        for c in word:
            if c in chars:
                continue
            else:
                chars.append(c)
            score += letters[c]
        if score > max_score:
            max_score = score
            best_guess = word
    return best_guess

def guess():
    word = input("word: ")
    present = [p.strip() for p in input("present: ").split(",") if p.strip() != '']
    fixed = [p.strip() for p in input("correct: ").split(",") if p.strip() != '']
    print()
    for i, c in enumerate(word):
        if c not in fixed and c not in present:
            hints['wrong'].append(c)
        elif c in fixed:
            hints['fixed'].append((c, i))
        elif c in present:
            hints['present'].append((c, i))
    possible_guesses = [w for w in possible_words if condition(w, hints)]
    print("possible solutions are", possible_guesses)
    if len(possible_guesses) > 1:
        print("the best word to gather information is", gather_info())
        
    return possible_guesses