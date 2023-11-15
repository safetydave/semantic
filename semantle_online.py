import random

from cohort_bayes_solver import CohortBayesSolver
from gradient_solver import GradientSolver
import similarity_model as sm
import vocabulary as voc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


class SemantleOnline:

    def __init__(self):
        self.vocabulary = voc.VocabularyUF()
        self.vocabulary.remove_nsfw_words()
        self.similarity = sm.SimilarityModelUSE(self.vocabulary)
        self.solver = GradientSolver(self.similarity, log=True)
        self.driver = self.init_driver()

    @staticmethod
    def init_driver():
        driver = webdriver.Firefox()
        driver.get("https://semantle.com")
        assert "Semantle" in driver.title
        try:
            SemantleOnline.try_auto_close_rules(driver)
        except:
            input('please close rules dialog and press enter to continue')
        return driver

    @staticmethod
    def try_auto_close_rules(driver):
        try:
            elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rules-close")))
        finally:
            driver.find_element(By.ID, "rules-close").click()

    def merge_guesses(self, guesses, scores):
        unmerged = []
        for i, gw in enumerate(guesses):
            merged = False
            if gw in self.solver.similarity.vocab_words:
                gi = self.solver.similarity.word_index(gw)
                if not self.solver.guess_merged(gi):
                    self.solver.merge_guess(gi, scores[i], 100)
                    merged = True
            if not merged:
                unmerged.append(i)
        return unmerged

    def live_guess(self, guess):
        guess_input = self.driver.find_element(By.ID, "guess")
        guess_input.send_keys(guess)
        guess_input.send_keys(Keys.RETURN)

    def guess_missed(self):
        guess_error = self.driver.find_element(By.ID, "error")
        return guess_error.is_displayed()

    def clear_guess(self):
        guess_input = self.driver.find_element(By.ID, "guess")
        guess_input.clear()

    def get_scores(self):
        guess_table = self.driver.find_element(By.ID, "guesses")
        rows = guess_table.find_elements(By.TAG_NAME, "tr")
        guesses = []
        scores = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                guesses.append(cols[1].text)
                scores.append(float(cols[2].text))
        return guesses, scores

    def solve(self):
        guesses, scores = [], []
        while not (len(scores) > 0 and max(scores) > 99.9):
            guess = self.solver.similarity.word_string(self.solver.make_guess())
            print(guess)
            self.live_guess(guess)
            time.sleep(1)
            missed = self.guess_missed()
            if missed: self.solver.merge_guess(self.solver.similarity.word_index(guess), 0, 100)
            self.clear_guess()
            if missed: time.sleep(1)
            try:
                guesses, scores = self.get_scores()
            except StaleElementReferenceException:
                pass
            finally:
                self.merge_guesses(guesses, scores)
        return guesses, scores

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    online = SemantleOnline()
    g, s = online.solve()
    print(g[-1])
    online.close()
