from abc import abstractmethod


class AlphaBase:
    # 返回因子集的fields, names
    def get_label(self):
        return "qcut(shift(close, -1)/close - 1,3)", 'label'

    @abstractmethod
    def get_factors(self):
        pass

    def get_field_by_name(self, name):
        fields, names = self.get_factors()
        for f,n in zip(fields, names):
            if n == name:
                return f

    #def get_labels(self):
    #    return ["label(shift(close, -1)/close - 1,0)"], ['label']

    def get_ic_labels(self):
        days = [1, 5, 10, 20]
        fields = ['shift(close, -{})/close - 1'.format(d) for d in days]
        names = ['return_{}'.format(d) for d in days]
        return fields, names

    def get_all_features_names(self):
        fields, names = self.get_fields_names()
        label_field, label_name = self.get_label()

        all_fields = fields.copy()
        all_fields.append(label_field)

        all_names = names.copy()
        all_names.append(label_name)
        return all_fields, all_names


class AlphaLit(AlphaBase):


    def get_fields_names(self):
        fields = []
        names = []

        windows = [2, 5, 10, 20]
        fields += ['close/shift(close,%d) - 1' % d for d in windows]
        names += ['roc_%d' % d for d in windows]

        fields += ['avg(volume,1)/avg(volume,5)']
        names += ['avg_amount_1_avg_amount_5']

        fields += ['avg(volume,5)/avg(volume,20)']
        names += ['avg_amount_5_avg_amount_20']

        fields += ['rank(avg(volume,1))/rank(avg(volume,5))']
        names += ['rank_avg_amount_1_avg_amount_5']

        fields += ['avg(volume,5)/avg(volume,20)']
        names += ['rank_avg_amount_5_avg_amount_20']

        windows = [2, 5, 10]
        fields += ['rank(roc_%d)' % d for d in windows]
        names += ['rank_roc_%d' % d for d in windows]

        fields += ['rank(roc_2)/rank(roc_5)']
        names += ['rank_roc_2_rank_roc_5']

        fields += ['rank(roc_5)/rank(roc_10)']
        names += ['rank_roc_5_rank_roc_10']

        return fields, names

    def get_label(self):
        return "qcut(shift(close, -1)/close - 1,3)", 'label'



