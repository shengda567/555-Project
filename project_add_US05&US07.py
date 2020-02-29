"""Cornerstone Project 03"""
from prettytable import PrettyTable
from datetime import date


class Individual:
    def __init__(self):
        self.indi_dict = {}
    def draw_pretty_table(self):
        pt = PrettyTable()
        pt.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
        for indi in self.indi_dict:
            alive = True
            death_date = 'NA'
            if self.indi_dict[indi]['DEAT'] != 'NA':
                alive = False
                death_date = self.indi_dict[indi]['DEAT']
            pt.add_row([indi, self.indi_dict[indi]['NAME'], self.indi_dict[indi]['SEX'], self.indi_dict[indi]['BIRT'], ageCalculator(self.indi_dict[indi]['BIRT']), alive, death_date, self.indi_dict[indi]['FAMC'], self.indi_dict[indi]['FAMS']])
        print(pt)

class Family:
    def __init__(self):
        self.family_dict = {}
    def draw_pretty_table(self):
        pt = PrettyTable()
        pt.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
        for fam in self.family_dict:
            pt.add_row([fam, self.family_dict[fam]['MARR'], self.family_dict[fam]['DIV'], self.family_dict[fam]['HUSB'][0], self.family_dict[fam]['HUSB'][1], self.family_dict[fam]['WIFE'][0], self.family_dict[fam]['WIFE'][1], self.family_dict[fam]['CHIL']])
        print(pt)


"""File Filter"""
def filter_file(file_to_filter):
    valid_tags_for_0 = ['HEAD', 'TRLR', 'NOTE']
    valid_tags_for_1 = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
    valid_tags_for_2 = ['DATE']

    filtered_lines = []

    for line in file_to_filter:
        if line == '':
            continue
        else:
            line = line.strip('\n')
            line_list = line.split(' ')
            '''new organized line in the form of list'''
            new_line = []

            '''find INDI and FAM'''
            if line_list[0] == '0':
                if 'INDI' in line.split(' '):
                    new_line = ['0', 'INDI', 'Y', line_list[1]] if line_list[1] != 'INDI' else ['0', 'INDI', 'N', line_list[2]]
                elif 'FAM' in line.split(' '):
                    new_line = ['0', 'FAM', 'Y', line_list[1]] if line_list[1] != 'FAM' else ['0', 'FAM', 'N', line_list[2]]
                else:
                    if line_list[1] in valid_tags_for_0:
                        new_line = line.split(' ', 2)
                        new_line.insert(2, 'Y')
                    else:
                        new_line = line.split(' ', 2)
                        new_line.insert(2, 'N')
            elif line[0] == '1':
                if line_list[1] in valid_tags_for_1:
                    new_line = line.split(' ', 2)
                    new_line.insert(2, 'Y')
                else:
                    new_line = line.split(' ', 2)
                    new_line.insert(2, 'N')
            elif line[0] == '2':
                if line_list[1] in valid_tags_for_2:
                    new_line = line.split(' ', 2)
                    new_line.insert(2, 'Y')
                else:
                    new_line = line.split(' ', 2)
                    new_line.insert(2, 'N')
            if new_line[2] == 'Y':
                filtered_lines.append('|'.join(new_line))
    print(filtered_lines)
    return filtered_lines

def draw_skeleton(filtered_file, individual, family):
    '''takes the filtered file, the individual object and the remily object, will draw the skeleton with NA'''
    for line in filtered_file:
            line = line.split('|')
            if line[0] == '0' and line[1] == 'INDI':
                indi_id = line[3]
                individual.indi_dict[indi_id] = {'NAME': 'NA', 'SEX': 'NA', 'BIRT': 'NA', 'DEAT': 'NA', 'FAMC': 'NA', 'FAMS': 'NA'}
            if line[0] == '0' and line[1] == 'FAM':
                fam_id = line[3]
                family.family_dict[fam_id] = {'MARR': 'NA', 'HUSB': 'NA', 'WIFE': 'NA', 'CHIL': set(), 'DIV': 'NA'}

def fill_skeleton(filtered_file, individual, family):
    '''takes the filtered file, the individual object and the remily object, will fill the skeleton drawn'''
    # for lines after 0 INDI and 0 FAM
    saved_value = {'indi_id': '', 'fam_id': '', 'name': '', 'date_flag': ''}
    for line in filtered_file:
        line = line.split('|')
        if line[0] == '0' and line[1] == 'INDI':
            saved_value['indi_id'] = line[3]
        elif line[0] == '0' and line[1] == 'FAM':
            saved_value['fam_id'] = line[3]

        '''0 INDI situation'''
        if line[0] == '1' and line[1] == 'NAME':
            individual.indi_dict[saved_value['indi_id']]['NAME'] = line[3]
            saved_value['name'] = line[3]
        elif line[0] == '1' and line[1] == 'SEX':
            individual.indi_dict[saved_value['indi_id']]['SEX'] = line[3]
        elif line[0] == '1' and line[1] == 'BIRT':
            saved_value['date_flag'] = 'BIRT'
        elif line[0] == '1' and line[1] == 'DEAT':
            saved_value['date_flag'] = 'DEAT'
        elif line[0] == '1' and line[1] == 'FAMC':
            individual.indi_dict[saved_value['indi_id']]['FAMC'] = line[3]
            family.family_dict[line[3]]['CHIL'].add(saved_value['indi_id'])
        elif line[0] == '1' and line[1] == 'FAMS':
            individual.indi_dict[saved_value['indi_id']]['FAMS'] = line[3]
            if individual.indi_dict[saved_value['indi_id']]['SEX'] == 'M':
                family.family_dict[line[3]]['HUSB'] = [saved_value['indi_id'], saved_value['name']]
            elif individual.indi_dict[saved_value['indi_id']]['SEX'] == 'F':
                family.family_dict[line[3]]['WIFE'] = [saved_value['indi_id'], saved_value['name']]

        '''0 FAM situation'''
        if line[0] == '1' and line[1] == 'MARR':
            saved_value['date_flag'] = 'MARR'
        elif line[0] == '1' and line[1] == 'DIV':
            saved_value['date_flag'] = 'DIV'

        '''fill in the date'''
        if line[0] == '2' and line[1] == "DATE":
            if saved_value['date_flag'] == 'BIRT' or saved_value['date_flag'] == 'DEAT':
                individual.indi_dict[saved_value['indi_id']][saved_value['date_flag']] = dateParser(line[3])
            elif saved_value['date_flag'] == 'MARR' or saved_value['date_flag'] == 'DIV':
                family.family_dict[saved_value['fam_id']][saved_value['date_flag']] = dateParser(line[3])

def dateParser(year):
    dat = year.split(" ")
    month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    yr = dat[2]
    mn = month_dict[dat[1]]
    dy = dat[0]
    return f"{yr}-{mn}-{dy}"

def ageCalculator(birthDate):
    today = date.today()
    year, month, day = birthDate.split("-")
    return today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))



#User Story 05
def marriage_before_death(individual_repo, family_repo):
    US05_report = {}

    for fam in family_repo.family_dict:
        husband_ID = family_repo.family_dict[fam]['HUSB'][0]
        wife_ID = family_repo.family_dict[fam]['WIFE'][0]
        marriage_date = family_repo.family_dict[fam]['MARR']

        husband_death_date = individual_repo.indi_dict[husband_ID]['DEAT']
        wife_death_date = individual_repo.indi_dict[wife_ID]['DEAT']

        if husband_death_date == 'NA' and wife_death_date == 'NA':
            US05_report[fam] = True
        elif husband_death_date != 'NA' and wife_death_date == 'NA':
            US05_report[fam] = husband_death_date >= marriage_date
        elif wife_death_date != 'NA' and husband_death_date == 'NA':
            US05_report[fam] = wife_death_date >= marriage_date
        else:
            first_death_date = husband_death_date if husband_death_date <= wife_death_date else wife_death_date
            US05_report[fam] = first_death_date >= marriage_date
        #print(Marry_before_death_dict)

#User Story 07
def less_150_years_old(individual_repo):
    US07_report = {}
    for indi in individual_repo.indi_dict:
        indi_death_date = individual_repo.indi_dict[indi]['DEAT']
        indi_birth_date = individual_repo.indi_dict[indi]['BIRT']

        if indi_death_date != 'NA':
            today = date.today()
            year, month, day = indi_birth_date.split("-")
            year_dif = today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))
            if year_dif > 150:
                US07_report[indi] = False
            else:
                US07_report[indi] = True
        else:
            if ageCalculator(indi_birth_date) > 150:
                US07_report[indi] = False
            else:
                US07_report[indi] = True
    #print(US07_report)



"""Main Function Entry Point"""
def main():
    file_path = "Hercule-Poirot.ged"
    with open(file_path, 'r') as file:
        unfiltered_file = file.readlines()
        '''filter the file so only valid lines are returned'''
        filtered_file = filter_file(unfiltered_file)
        '''draw the skeleton of Individual and Family and assign each field with NA'''
        individual = Individual()
        family = Family()

        """ Add User Stories here"""



        draw_skeleton(filtered_file, individual, family)
        fill_skeleton(filtered_file, individual, family)

        """Shengda's US05 and US07 have to be here"""
        marriage_before_death(individual, family)
        less_150_years_old(individual)

        individual.draw_pretty_table()
        family.draw_pretty_table()


    #print(family.family_dict)
if __name__ == '__main__':
    main()
