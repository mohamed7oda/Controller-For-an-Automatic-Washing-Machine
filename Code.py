!pip install -U scikit-fuzzy
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


dirt = ctrl.Antecedent(np.arange(0, 101, 1), 'dirt')
softness_fabric = ctrl.Antecedent(np.arange(0, 101, 1), 'softness_fabric')
amount_clothes = ctrl.Antecedent(np.arange(1, 51, 1), 'amount_clothes')
amount_soup = ctrl.Consequent(np.arange(0.1, 0.9, 0.1), 'amount_soup')
time = ctrl.Consequent(np.arange(0, 61, 1), 'time')


dirt["small"] = fuzz.trapmf(dirt.universe, [0, 0, 20, 40])
dirt["medium"] = fuzz.trapmf(dirt.universe, [20, 40, 60, 80])
dirt["large"] = fuzz.trapmf(dirt.universe, [60, 80, 100, 100])

softness_fabric['soft'] = fuzz.trapmf(softness_fabric.universe, [0, 0, 20, 40])
softness_fabric['ordinary'] = fuzz.trapmf(softness_fabric.universe, [20, 40, 60, 80])
softness_fabric['stiff'] = fuzz.trapmf(softness_fabric.universe, [60, 80, 100, 100])

amount_clothes['small'] = fuzz.trapmf(amount_clothes.universe, [1, 1, 10, 20])
amount_clothes['medium'] = fuzz.trapmf(amount_clothes.universe, [10, 20, 30, 40])
amount_clothes['large'] = fuzz.trapmf(amount_clothes.universe, [30, 40, 50, 50])

amount_soup['small'] = fuzz.trapmf(amount_soup.universe, [0.1, 0.1, 0.2, 0.4])
amount_soup['medium'] = fuzz.trapmf(amount_soup.universe, [0.2, 0.4, 0.6, 0.8])
amount_soup['large'] = fuzz.trapmf(amount_soup.universe, [0.6, 0.8, 0.9, 0.9])

time['very_short'] = fuzz.trapmf(time.universe, [0, 0, 10, 15])
time['short'] = fuzz.trapmf(time.universe, [10, 15, 20, 25])
time['standard'] = fuzz.trapmf(time.universe, [20, 25, 30, 35])
time['long'] = fuzz.trapmf(time.universe, [30, 35, 40, 45])
time['very_long'] = fuzz.trapmf(time.universe, [40, 45, 50, 60])


rule1 = ctrl.Rule(dirt['small'] & softness_fabric['soft'], time['very_short'])
rule2 = ctrl.Rule(dirt['medium'] & softness_fabric['ordinary'], time['standard'])
rule3 = ctrl.Rule(dirt['small'] & (softness_fabric ['ordinary'] | softness_fabric ['stiff']), time['short'])
rule33 = ctrl.Rule(dirt['medium'] & softness_fabric['soft'], time['short'])
rule4 = ctrl.Rule(dirt['medium'] & softness_fabric['stiff'], time['long'])
rule5 = ctrl.Rule(dirt['large'] & (softness_fabric['ordinary'] | softness_fabric['stiff']), time['very_long'])
rule6 = ctrl.Rule(dirt['large'] & softness_fabric['soft'], time['standard'])
rule7 = ctrl.Rule(dirt['small'] & softness_fabric['soft'], time['short'])
rule8 = ctrl.Rule((dirt['medium'] | dirt['large']) & (softness_fabric['ordinary'] | softness_fabric['stiff']), time['long'])


rule12 = ctrl.Rule(amount_clothes['large'], amount_soup['large'])
rule22 = ctrl.Rule(amount_clothes['small'], amount_soup['small'])
rule32 = ctrl.Rule(amount_clothes['medium'], amount_soup['medium'])


x= int(input('Enter the percentage of dirt (from 0 to 100): '))
y= int(input('Enter the softness of the fabric (from 0 to 100): '))
time_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule33, rule4, rule5, rule6, rule7, rule8])
time_sim = ctrl.ControlSystemSimulation(time_ctrl)
time_sim.input['dirt'] = x
time_sim.input['softness_fabric'] = y



time_sim.compute()
time_output = time_sim.output['time']
print('Time: ', time_output ,'minutes ', '\n')
time.view()


z= int(input('Enter the amount of clothes (from 1 to 50): '))
soup_ctrl = ctrl.ControlSystem([rule12, rule22, rule32])
soup_sim = ctrl.ControlSystemSimulation(soup_ctrl)
soup_sim.input['amount_clothes'] = z


soup_sim.compute()
soup_output = soup_sim.output['amount_soup']
print('Amount of soup: ', soup_output )
amount_soup.view()
