"""

Classify el image by rule condition.

"""
import yaml


class RuleEngine:

    def __init__(self, config):
        """
        Init RuleEngine var config filename

        Args:
            config: str, config filename
        """
        self.config = yaml.load(open(config, 'r', encoding='utf-8').read(), yaml.FullLoader)
    
    def clear_number_count(self):
        for defect_category in self.config['defect']:
            for level in self.config['defect'][defect_category]['level']:
                self.items_handle_clear_number_count(items=self.config['defect'][defect_category]['level'][level]['items'])
    
    def items_handle_clear_number_count(self, items):
        for item in items:
            if "items" in item:
                self.items_handle_clear_number_count(items=item['items'])
            else:
                if "number_count" in item['metas']:
                    item['metas']['number_count'] = 0

    def defect_handle(self, defects):
        """
        Handle a list of defects in one image

        Args:
            defects: dict, defect to handle
        """
        # clear defect number count cross image
        self.clear_number_count()

        defect_level_good_to_bad = self.config['defect_level_good_to_bad']
        record_defect_level = self.config['record_defect_level']
        # lowest level cross image
        worst_level_total = None
        worst_level_total_index = 0
        worst_level_total_defect_index = []
        # all defects
        defects_level_index = []

        # Firstly, count the number of confirmative defect by defect category and level
        for defect in defects:
            for defect_category in self.config['defect']:
                if defect['category'] == defect_category: 
                    for level in self.config['defect'][defect_category]['level']:
                        logic = self.config['defect'][defect_category]['level'][level]['logic']
                        items = self.config['defect'][defect_category]['level'][level]['items']
                        self.logic_handle(
                            defect=defect, logic=logic, items=items, include_meta_number=False)
                # elif defect['category'] == defect_category == 'HB':
                #     pass


        # Secondly, classify image var metas(include the number of metas)
        for di in range(len(defects)):
            defect = defects[di]
            for defect_category in self.config['defect']:
                if defect['category'] == defect_category:
                    worst_level_in_one_defect = None
                    current_level_defect_index = []  # seems there is no need to be a list, rather than be a int

                    for level in self.config['defect'][defect_category]['level']:
                        logic = self.config['defect'][defect_category]['level'][level]['logic']
                        items = self.config['defect'][defect_category]['level'][level]['items']
                        if self.logic_handle(defect=defect, logic=logic, items=items, include_meta_number=True) is True:
                            if worst_level_in_one_defect is None:
                                worst_level_in_one_defect = level
                                current_level_defect_index = [di]
                            elif defect_level_good_to_bad.index(level) == defect_level_good_to_bad.index(worst_level_in_one_defect):
                                current_level_defect_index.append(di)
                            elif defect_level_good_to_bad.index(level) > defect_level_good_to_bad.index(worst_level_in_one_defect):
                                worst_level_in_one_defect = level
                                current_level_defect_index = [di]
        
                    # set default level if there is no level was choosen by rule
                    if worst_level_in_one_defect is None:
                        worst_level_in_one_defect = self.config['defect'][defect_category]['default_level']
                        current_level_defect_index = [di]
                    # update level info cross image
                    if defect_level_good_to_bad.index(worst_level_in_one_defect) > worst_level_total_index:
                        worst_level_total_index = defect_level_good_to_bad.index(worst_level_in_one_defect)
                        worst_level_total_defect_index = current_level_defect_index
                    elif defect_level_good_to_bad.index(worst_level_in_one_defect) == worst_level_total_index:
                        worst_level_total_defect_index += current_level_defect_index
                    defects_level_index.append(self.config['defect_level_good_to_bad'].index(worst_level_in_one_defect))

        worst_level_total = defect_level_good_to_bad[worst_level_total_index]
        if worst_level_total not in record_defect_level:
            worst_level_total_defect_index = []
        
        return worst_level_total, worst_level_total_defect_index, defects_level_index

    @staticmethod
    def meta_handle(defect, meta_key, meta_spec):
        """
        Is defect's attribute between spec high and spec low

        Args:
            defect: dict, defect to handle
            meta_key: str, key name of meta info
            meta_spec: list, spec of meta info

        Returns: Ture or False

        """
        # assert hasattr(defect, meta_key)

        if meta_spec[0] <= defect[meta_key] <= meta_spec[1]:
            return True
        else:
            return False

    def logic_handle(self, defect, logic, items, include_meta_number):
        """
        Logical operations between items

        Args:
            defect: dict, defect to handle
            logic: str, key name of meta info
            items: list, spec of meta info

        Returns: True or False
        """
        if logic == 'AND':
            logic_bool = True
        elif logic == 'OR':
            logic_bool = False
        for item in items:
            if ('logic' in item):
                sub_logic = self.logic_handle(defect=defect, logic=item['logic'], items=item['items'], include_meta_number=include_meta_number)
                if logic == 'AND':
                    logic_bool = logic_bool and sub_logic
                elif logic == 'OR':
                    logic_bool = logic_bool or sub_logic
            else:
                metas_bool = True
                metas = item['metas']
                for meta_key in metas:
                    if (not include_meta_number) and (meta_key in ["number", "number_count"]):
                        continue
                    elif include_meta_number:

                        if meta_key == "number":
                            metas_bool = metas_bool and self.meta_handle({"number": metas["number_count"]},
                                                                            meta_key=meta_key, meta_spec=metas[meta_key])
                        elif meta_key not in ["number", "number_count"]:
                            metas_bool = metas_bool and self.meta_handle(defect,
                                                                             meta_key=meta_key, meta_spec=metas[meta_key])
                    else:
                        metas_bool = metas_bool and self.meta_handle(defect,
                                                                     meta_key=meta_key, meta_spec=metas[meta_key])
                if (not include_meta_number) and ("number" in metas):
                    if "number_count" not in metas:
                        metas['number_count'] = 1 if metas_bool else 0
                    else:
                        if metas_bool:
                            metas['number_count'] += 1
                
                if logic == "AND":
                    logic_bool = logic_bool and metas_bool
                elif logic == "OR":
                    logic_bool = logic_bool or metas_bool
                    # if logic_bool is True:
                    #     return logic_bool
        return logic_bool


if __name__ == "__main__":
    ruleEngine = RuleEngine(config='rule_engine_config.yaml')
