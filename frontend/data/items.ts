export interface MenuItem {
  name: string;
  price: number;
  unit: string;
}

export interface ItemsCatalog {
  [category: string]: MenuItem[];
}

export const itemsCatalog: ItemsCatalog = {
  Grocery: [
    { name: "White Bread", price: 20, unit: "piece" },
    { name: "Bhuja Chana", price: 100, unit: "kg" },
    { name: "Maggie (Small - 75g)", price: 15, unit: "packet" },
    { name: "Maggie (Family Pack - 400g)", price: 56, unit: "packet" },
    { name: "Moongfali", price: 160, unit: "kg" },
    { name: "Soyabean (Packet)", price: 10, unit: "packet" },
    { name: "Soyabean (Open - Small)", price: 100, unit: "kg" },
    { name: "Macaroni / Pasta", price: 60, unit: "kg" },
    { name: "Sugar (Chini)", price: 45, unit: "kg" },
    { name: "Glucose D (200g)", price: 56, unit: "packet" },
    { name: "Glucose D (400g)", price: 89, unit: "packet" },
    { name: "Jam (Small)", price: 25, unit: "bottle" },
    { name: "Jam (Big)", price: 90, unit: "bottle" },
    { name: "Colgate (Small)", price: 20, unit: "piece" },
    { name: "Colgate (Medium)", price: 70, unit: "piece" },
    { name: "Colgate (Big)", price: 130, unit: "piece" },
    { name: "Closeup (Small)", price: 20, unit: "piece" },
    { name: "Closeup (Big)", price: 55, unit: "piece" },
    { name: "Sensodyne Toothpaste", price: 140, unit: "piece" },
    { name: "Coffee (Nescafe - 50g)", price: 10, unit: "packet" },
    { name: "Coffee (Nescafe - 100g)", price: 124, unit: "packet" },
    { name: "Coffee (Nescafe - 200g)", price: 235, unit: "packet" },
    { name: "Mustard Oil (Sarso Tel)", price: 180, unit: "liter" },
    { name: "Fortune Oil", price: 190, unit: "liter" },
    { name: "Garam Masala (Whole)", price: 20, unit: "packet" },
    { name: "Garam Masala (Packet)", price: 10, unit: "packet" },
    { name: "Kacha Chana", price: 80, unit: "kg" },
    { name: "Makhana", price: 130, unit: "100 gm" },
    { name: "Kaju (Cashew)", price: 1000, unit: "kg" },
    { name: "Badam (Almond)", price: 1000, unit: "kg" },
    { name: "Pista (Packet)", price: 350, unit: "packet" },
  ],
  Stationary: [
    { name: "Practical File (Physics - 30 Pages)", price: 30, unit: "piece" },
    { name: "Practical File (Physics - 60 Pages)", price: 60, unit: "piece" },
    { name: "Practical File (Chemistry - 30 Pages)", price: 30, unit: "piece" },
    { name: "Practical File (Chemistry - 60 Pages)", price: 60, unit: "piece" },
    { name: "Practical File (General - 30 Pages)", price: 30, unit: "piece" },
    { name: "Practical File (General - 60 Pages)", price: 60, unit: "piece" },
    { name: "Pen (Cheap)", price: 4, unit: "piece" },
    { name: "Pen (Medium)", price: 5, unit: "piece" },
    { name: "Pen (Good)", price: 10, unit: "piece" },
    { name: "Pencil", price: 5, unit: "piece" },
    { name: "Eraser", price: 5, unit: "piece" },
    { name: "Sharpener", price: 5, unit: "piece" },
    { name: "Drawing Book (A3 - 36 pages)", price: 90, unit: "piece" },
    { name: "Drawing Book (A3 - 56 pages)", price: 110, unit: "piece" },
    { name: "A4 Size Pages (500 sheets)", price: 200, unit: "pack" },
    { name: "Stapler", price: 50, unit: "piece" },
    { name: "Staple Pins", price: 10, unit: "box" },
    { name: "Sticky Notes", price: 20, unit: "pack" },
    { name: "Fevicol (Small)", price: 10, unit: "bottle" },
    { name: "Fevicol (Medium)", price: 20, unit: "bottle" },
    { name: "Fevicol (Big)", price: 50, unit: "bottle" },
    { name: "Double-Sided Tape (Small)", price: 5, unit: "roll" },
    { name: "Double-Sided Tape (Big)", price: 10, unit: "roll" },
    { name: "Spiral Notebook (Plain - 100 Pages)", price: 80, unit: "piece" },
    { name: "Spiral Notebook (Plain - 200 Pages)", price: 100, unit: "piece" },
    { name: "Spiral Notebook (Lined - 100 Pages)", price: 80, unit: "piece" },
    { name: "Register (A4 Rough - 100 Pages)", price: 30, unit: "piece" },
    { name: "Register (A4 Rough - 200 Pages)", price: 40, unit: "piece" },
    { name: "Graph Book", price: 10, unit: "piece" },
    { name: "Cello Tape", price: 5, unit: "roll" },
    { name: "Highlighter", price: 20, unit: "piece" },
  ],
  Fruits: [
    { name: "Banana", price: 40, unit: "kg" },
    { name: "Pomegranate (Anaar)", price: 180, unit: "kg" },
    { name: "Mango", price: 100, unit: "kg" },
    { name: "Apple", price: 200, unit: "kg" },
    { name: "Orange (Santara)", price: 150, unit: "kg" },
    { name: "Papaya (Papita)", price: 60, unit: "kg" },
    { name: "Kiwi", price: 50, unit: "piece" },
    { name: "Coconut (Nariyal)", price: 70, unit: "piece" },
    { name: "Grapes (Angoor)", price: 150, unit: "kg" },
  ],
};

export const DELIVERY_CHARGE = 15;

export const HOSTEL_OPTIONS = [
  { value: 'BH1', label: 'BH1 (Boys Hostel 1)' },
  { value: 'BH2', label: 'BH2 (Boys Hostel 2)' },
  { value: 'BH3', label: 'BH3 (Boys Hostel 3)' },
  { value: 'GH1', label: 'GH1 (Girls Hostel)' },
];