import pandas as pd
import numpy as np
from collections import defaultdict

class AprioriAll:
    def __init__(self, min_sup=0.05, max_gap=None):
        self.min_sup = min_sup
        self.max_gap = max_gap
        self.sequences = []
        self.frequent_patterns = {}
        
    def load_data(self, filepath):
        """Загрузка и преобразование данных"""
        df = pd.read_csv(filepath, encoding='latin1')
        df = df.dropna(subset=['CustomerID', 'InvoiceDate'])
        df = df[df['Quantity'] > 0]
        
        df['Date'] = pd.to_datetime(df['InvoiceDate']).dt.date
        
        # Группируем товары внутри транзакции
        df_grouped = df.groupby(['CustomerID', 'InvoiceNo', 'Date'])['Description'].apply(
            lambda x: tuple(sorted(set(x)))
        ).reset_index()
        
        # Формируем последовательности клиентов
        self.sequences = []
        for cust_id, group in df_grouped.groupby('CustomerID'):
            group = group.sort_values('Date')
            seq = []
            prev_date = None
            
            for _, row in group.iterrows():
                # Проверка временного окна
                if self.max_gap and prev_date:
                    gap = (row['Date'] - prev_date).days
                    if gap > self.max_gap:
                        seq = []  # Сбрасываем последовательность
                seq.append(row['Description'])
                prev_date = row['Date']
            
            if len(seq) >= 1:
                self.sequences.append(seq)
        
        return self.sequences
    
    def _is_subsequence(self, seq, pattern):
        """Проверка, является ли pattern подпоследовательностью seq"""
        pos = 0
        for elem in pattern:
            found = False
            for i in range(pos, len(seq)):
                if elem == seq[i]:
                    found = True
                    pos = i + 1
                    break
            if not found:
                return False
        return True
    
    def fit(self, sequences=None, filepath=None):
        """Запуск алгоритма AprioriAll"""
        if filepath:
            self.load_data(filepath)
        elif sequences:
            self.sequences = sequences
            
        if not self.sequences:
            raise ValueError("Нет данных для обучения")
            
        n_clients = len(self.sequences)
        min_sup_count = n_clients * self.min_sup
        
        # Поиск частых элементов (длина 1)
        item_counts = defaultdict(int)
        for seq in self.sequences:
            items_in_seq = set()
            for trans in seq:
                if isinstance(trans, tuple):
                    items_in_seq.update(trans)
                else:
                    items_in_seq.add(trans)
            for item in items_in_seq:
                item_counts[item] += 1
        
        freq_1 = { (item,): count for item, count in item_counts.items() 
                  if count >= min_sup_count }
        self.frequent_patterns.update(freq_1)
        
        return self.frequent_patterns
    
    def get_patterns_by_length(self, length):
        """Получить паттерны заданной длины"""
        return {k: v for k, v in self.frequent_patterns.items() 
                if len(k) == length}
