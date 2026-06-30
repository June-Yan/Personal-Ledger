export interface User {
  id: number;
  email: string;
}

export interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  icon?: string;
  sort_order: number;
  is_preset: boolean;
}

export interface Bill {
  id: number;
  amount: number;
  category_id: number;
  category_name: string;
  category_type: 'income' | 'expense';
  note?: string;
  bill_date: string;
  created_at?: string;
}

export interface MonthlySummary {
  income_total: number;
  expense_total: number;
  balance: number;
}

export interface CategoryBreakdown {
  category_id: number;
  category_name: string;
  amount: number;
  percentage: number;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}
