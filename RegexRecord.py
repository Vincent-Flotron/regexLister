
class RegexRecordsList:
    def __init__(self, regex_records=None, fields_names=None):
        if regex_records is None:
            regex_records = []
        self.regex_records = regex_records

        if fields_names is None:
            fields_names = []
        self.fields_names = fields_names

    def add_a_field_name(self, field_name):
        self.fields_names.append(field_name)

    def sort_by_match_score_desc(self):
        self.regex_records.sort(key=lambda x: x.match_score, reverse=True)
        self.regex_records.sort(key=lambda x: x.match_score, reverse=True)

    def append(self, regex_record):
        self.regex_records.append(regex_record)

    def get_match_only(self):
        return RegexRecordsList([rc for rc in self.regex_records if rc.match_score > 0], fields_names=self.fields_names)
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.regex_records)
    
    def get_list_attribute_values(self, attribute_name):
        return [reg_rec.get_attribute(attribute_name) for reg_rec in self.regex_records]
    
    def get_field_names(self):
        return self.fields_names
    
    def complete_fields(self, record):
        for regex_record, record in zip(self.regex_records, record):
            if regex_record.id != record[0]:
                raise Exception(f"regex_record.id '{regex_record.id}' != record[0] '{record[0]}'")
            regex_record.search_regex      = record[2]
            regex_record.replacement_regex = record[3]

    def len(self):
        return len(self.regex_records)
    
    def items(self):
        return self.regex_records

class RegexRecord:
    def __init__(self, id, short_description, search_regex, replacement_regex, match_score):
        self.id                = id
        self.short_description = short_description
        self.search_regex      = search_regex
        self.replacement_regex = replacement_regex
        self.match_score       = match_score

    def get_attribute(self, attribute_name):
        return getattr(self, attribute_name)
    
    def get_all_attributes(self):
        return (self.id, self.short_description, self.search_regex, self.replacement_regex, self.match_score)

    def __str__(self):
        return f"id: {self.id}, short_description: {self.short_description}, search_regex: {self.search_regex}, replacement_regex: {self.replacement_regex}, match_score: {self.match_score}"
