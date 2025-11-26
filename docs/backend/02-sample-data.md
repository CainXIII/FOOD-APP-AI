# 📦 Sample Data - Database Seed Data

## Overview
File này chứa complete sample data để seed database cho development và testing. Data được chuẩn bị theo format SQL INSERT statements và JSON cho easy import.

**Usage:**
```bash
# Import via psql
psql -d cooking_assistant -f sample_data.sql

# Or via Python script
python scripts/seed_database.py
```

---

## 1. Categories

### SQL Insert Statements

```sql
-- Main Categories
INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, color_hex, sort_order) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Món chính', 'Main Dishes', 'main-dishes', 
 'Các món ăn chính trong bữa cơm', 'Main courses and entrees', 
 'https://storage.cooking.app/icons/main-dishes.svg', '#FF6F00', 1),

('550e8400-e29b-41d4-a716-446655440002', 'Món khai vị', 'Appetizers', 'appetizers',
 'Món ăn khai vị, món nhắm', 'Starters and small plates',
 'https://storage.cooking.app/icons/appetizers.svg', '#4CAF50', 2),

('550e8400-e29b-41d4-a716-446655440003', 'Món tráng miệng', 'Desserts', 'desserts',
 'Món ngọt, bánh, tráng miệng', 'Sweet dishes and desserts',
 'https://storage.cooking.app/icons/desserts.svg', '#E91E63', 3),

('550e8400-e29b-41d4-a716-446655440004', 'Món súp', 'Soups', 'soups',
 'Các loại súp, canh, lẩu', 'Soups and broths',
 'https://storage.cooking.app/icons/soups.svg', '#2196F3', 4),

('550e8400-e29b-41d4-a716-446655440005', 'Đồ uống', 'Beverages', 'beverages',
 'Nước uống, sinh tố, cocktail', 'Drinks and beverages',
 'https://storage.cooking.app/icons/beverages.svg', '#9C27B0', 5),

('550e8400-e29b-41d4-a716-446655440006', 'Món ăn sáng', 'Breakfast', 'breakfast',
 'Món ăn sáng, brunch', 'Breakfast and brunch dishes',
 'https://storage.cooking.app/icons/breakfast.svg', '#FF9800', 6),

('550e8400-e29b-41d4-a716-446655440007', 'Món salad', 'Salads', 'salads',
 'Salad rau củ, trộn', 'Fresh salads',
 'https://storage.cooking.app/icons/salads.svg', '#8BC34A', 7),

('550e8400-e29b-41d4-a716-446655440008', 'Món nướng', 'Grilled', 'grilled',
 'Món nướng, BBQ', 'Grilled and barbecue',
 'https://storage.cooking.app/icons/grilled.svg', '#FF5722', 8),

('550e8400-e29b-41d4-a716-446655440009', 'Món chiên', 'Fried', 'fried',
 'Món chiên giòn, rán', 'Fried dishes',
 'https://storage.cooking.app/icons/fried.svg', '#FFC107', 9),

('550e8400-e29b-41d4-a716-446655440010', 'Món hấp', 'Steamed', 'steamed',
 'Món hấp, dim sum', 'Steamed dishes',
 'https://storage.cooking.app/icons/steamed.svg', '#00BCD4', 10),

('550e8400-e29b-41d4-a716-446655440011', 'Món xào', 'Stir-fried', 'stir-fried',
 'Món xào, rim', 'Stir-fried dishes',
 'https://storage.cooking.app/icons/stir-fried.svg', '#F44336', 11),

('550e8400-e29b-41d4-a716-446655440012', 'Món hầm', 'Braised', 'braised',
 'Món hầm, kho, om', 'Braised and stewed',
 'https://storage.cooking.app/icons/braised.svg', '#795548', 12),

('550e8400-e29b-41d4-a716-446655440013', 'Bánh mì & Sandwich', 'Bread & Sandwiches', 'bread-sandwiches',
 'Bánh mì, sandwich các loại', 'Breads and sandwiches',
 'https://storage.cooking.app/icons/bread.svg', '#FFEB3B', 13),

('550e8400-e29b-41d4-a716-446655440014', 'Món chay', 'Vegetarian', 'vegetarian',
 'Món ăn chay, thuần chay', 'Vegetarian and vegan',
 'https://storage.cooking.app/icons/vegetarian.svg', '#66BB6A', 14),

('550e8400-e29b-41d4-a716-446655440015', 'Món Việt', 'Vietnamese', 'vietnamese',
 'Món ăn Việt Nam truyền thống', 'Traditional Vietnamese cuisine',
 'https://storage.cooking.app/icons/vietnamese.svg', '#D32F2F', 15);
```

### JSON Format

```json
{
  "categories": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name_vi": "Món chính",
      "name_en": "Main Dishes",
      "slug": "main-dishes",
      "description_vi": "Các món ăn chính trong bữa cơm",
      "description_en": "Main courses and entrees",
      "icon_url": "https://storage.cooking.app/icons/main-dishes.svg",
      "color_hex": "#FF6F00",
      "sort_order": 1
    }
  ]
}
```

---

## 2. Ingredients

### Common Vietnamese Ingredients

```sql
-- Proteins
INSERT INTO ingredients (id, name_vi, name_en, slug, aliases_vi, aliases_en, category, calories, protein_g, carbs_g, fat_g, is_vegetarian, is_vegan) VALUES
('650e8400-e29b-41d4-a716-446655440001', 'Xương bò', 'Beef bones', 'beef-bones',
 ARRAY['xương hầm', 'xương ống'], ARRAY['marrow bones', 'soup bones'],
 'meat', 150, 20, 0, 8, false, false),

('650e8400-e29b-41d4-a716-446655440002', 'Thịt bò', 'Beef', 'beef',
 ARRAY['thịt bò tươi', 'bò Úc'], ARRAY['beef meat', 'steak'],
 'meat', 250, 26, 0, 15, false, false),

('650e8400-e29b-41d4-a716-446655440003', 'Thịt gà', 'Chicken', 'chicken',
 ARRAY['gà ta', 'gà công nghiệp'], ARRAY['chicken breast', 'chicken meat'],
 'meat', 165, 31, 0, 3.6, false, false),

('650e8400-e29b-41d4-a716-446655440004', 'Thịt heo', 'Pork', 'pork',
 ARRAY['thịt lợn', 'thịt ba chỉ'], ARRAY['pork belly', 'pork meat'],
 'meat', 242, 27, 0, 14, false, false),

('650e8400-e29b-41d4-a716-446655440005', 'Tôm', 'Shrimp', 'shrimp',
 ARRAY['tôm sú', 'tôm thẻ'], ARRAY['prawns', 'shrimps'],
 'seafood', 99, 24, 0.2, 0.3, false, false),

('650e8400-e29b-41d4-a716-446655440006', 'Cá', 'Fish', 'fish',
 ARRAY['cá rô phi', 'cá chẽm'], ARRAY['tilapia', 'fish fillet'],
 'seafood', 128, 26, 0, 2.8, false, false),

('650e8400-e29b-41d4-a716-446655440007', 'Trứng gà', 'Chicken eggs', 'eggs',
 ARRAY['trứng', 'trứng tươi'], ARRAY['eggs', 'fresh eggs'],
 'dairy', 155, 13, 1.1, 11, true, false),

('650e8400-e29b-41d4-a716-446655440008', 'Đậu phụ', 'Tofu', 'tofu',
 ARRAY['đậu hũ', 'tàu hủ'], ARRAY['bean curd', 'soy tofu'],
 'protein', 76, 8, 1.9, 4.8, true, true);

-- Vegetables
INSERT INTO ingredients (id, name_vi, name_en, slug, aliases_vi, aliases_en, category, calories, protein_g, carbs_g, fat_g, is_vegetarian, is_vegan) VALUES
('650e8400-e29b-41d4-a716-446655440009', 'Gừng', 'Ginger', 'ginger',
 ARRAY['gừng tươi', 'củ gừng'], ARRAY['fresh ginger', 'ginger root'],
 'spices', 80, 1.8, 18, 0.8, true, true),

('650e8400-e29b-41d4-a716-446655440010', 'Hành tây', 'Onion', 'onion',
 ARRAY['hành khô', 'củ hành'], ARRAY['yellow onion', 'onions'],
 'vegetables', 40, 1.1, 9.3, 0.1, true, true),

('650e8400-e29b-41d4-a716-446655440011', 'Tỏi', 'Garlic', 'garlic',
 ARRAY['tỏi tây', 'củ tỏi'], ARRAY['garlic cloves', 'fresh garlic'],
 'spices', 149, 6.4, 33, 0.5, true, true),

('650e8400-e29b-41d4-a716-446655440012', 'Cà rót', 'Tomato', 'tomato',
 ARRAY['cà chua', 'cà'], ARRAY['tomatoes', 'fresh tomato'],
 'vegetables', 18, 0.9, 3.9, 0.2, true, true),

('650e8400-e29b-41d4-a716-446655440013', 'Cà rốt', 'Carrot', 'carrot',
 ARRAY['củ cà rốt'], ARRAY['carrots', 'fresh carrot'],
 'vegetables', 41, 0.9, 10, 0.2, true, true),

('650e8400-e29b-41d4-a716-446655440014', 'Khoai tây', 'Potato', 'potato',
 ARRAY['củ khoai', 'khoai tây tây'], ARRAY['potatoes', 'white potato'],
 'vegetables', 77, 2, 17, 0.1, true, true),

('650e8400-e29b-41d4-a716-446655440015', 'Rau muống', 'Water spinach', 'water-spinach',
 ARRAY['rau muống xào'], ARRAY['morning glory', 'kangkong'],
 'vegetables', 19, 2.6, 2.1, 0.2, true, true),

('650e8400-e29b-41d4-a716-446655440016', 'Rau ngót', 'Sweet leaf', 'sweet-leaf',
 ARRAY['rau ngót nấu canh'], ARRAY['sauropus', 'sweet leaf bush'],
 'vegetables', 45, 4.8, 6.3, 0.5, true, true),

('650e8400-e29b-41d4-a716-446655440017', 'Hành lá', 'Spring onion', 'spring-onion',
 ARRAY['hành tây tươi', 'hành lá tươi'], ARRAY['scallions', 'green onions'],
 'vegetables', 32, 1.8, 7.3, 0.2, true, true);

-- Noodles & Grains
INSERT INTO ingredients (id, name_vi, name_en, slug, aliases_vi, aliases_en, category, calories, protein_g, carbs_g, fat_g, is_vegetarian, is_vegan) VALUES
('650e8400-e29b-41d4-a716-446655440018', 'Bánh phở', 'Pho noodles', 'pho-noodles',
 ARRAY['bánh phở tươi', 'bánh phở khô'], ARRAY['rice noodles', 'flat rice noodles'],
 'grains', 109, 1.8, 25, 0.2, true, true),

('650e8400-e29b-41d4-a716-446655440019', 'Gạo', 'Rice', 'rice',
 ARRAY['gạo trắng', 'gạo tẻ'], ARRAY['white rice', 'jasmine rice'],
 'grains', 130, 2.7, 28, 0.3, true, true),

('650e8400-e29b-41d4-a716-446655440020', 'Bún', 'Rice vermicelli', 'rice-vermicelli',
 ARRAY['bún tươi', 'bún khô'], ARRAY['vermicelli noodles', 'thin rice noodles'],
 'grains', 109, 1.8, 24, 0.1, true, true),

('650e8400-e29b-41d4-a716-446655440021', 'Mì', 'Wheat noodles', 'wheat-noodles',
 ARRAY['mì trứng', 'mì tươi'], ARRAY['egg noodles', 'wheat noodles'],
 'grains', 138, 4.5, 25, 2.1, true, false);

-- Spices & Seasonings
INSERT INTO ingredients (id, name_vi, name_en, slug, aliases_vi, aliases_en, category, calories, protein_g, carbs_g, fat_g, is_vegetarian, is_vegan, allergens) VALUES
('650e8400-e29b-41d4-a716-446655440022', 'Muối', 'Salt', 'salt',
 ARRAY['muối biển', 'muối i-ốt'], ARRAY['sea salt', 'iodized salt'],
 'seasonings', 0, 0, 0, 0, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440023', 'Đường', 'Sugar', 'sugar',
 ARRAY['đường trắng', 'đường cát'], ARRAY['white sugar', 'granulated sugar'],
 'seasonings', 387, 0, 100, 0, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440024', 'Nước mắm', 'Fish sauce', 'fish-sauce',
 ARRAY['nước mắm Phú Quốc', 'nước mắm ngon'], ARRAY['Vietnamese fish sauce'],
 'seasonings', 35, 5.5, 3.5, 0, false, false, ARRAY['fish']),

('650e8400-e29b-41d4-a716-446655440025', 'Dầu ăn', 'Cooking oil', 'cooking-oil',
 ARRAY['dầu thực vật', 'dầu olive'], ARRAY['vegetable oil', 'olive oil'],
 'seasonings', 884, 0, 0, 100, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440026', 'Xì dầu', 'Soy sauce', 'soy-sauce',
 ARRAY['nước tương', 'xì dầu Nhật'], ARRAY['soy sauce', 'shoyu'],
 'seasonings', 53, 5.5, 4.9, 0.1, true, true, ARRAY['soy', 'gluten']),

('650e8400-e29b-41d4-a716-446655440027', 'Hạt nêm', 'Seasoning powder', 'seasoning-powder',
 ARRAY['bột ngọt', 'hạt nêm Knorr'], ARRAY['MSG', 'seasoning granules'],
 'seasonings', 80, 5, 15, 0, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440028', 'Tiêu', 'Black pepper', 'black-pepper',
 ARRAY['tiêu đen', 'hạt tiêu'], ARRAY['pepper', 'peppercorns'],
 'spices', 251, 10.4, 64, 3.3, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440029', 'Ớt', 'Chili pepper', 'chili',
 ARRAY['ớt hiểm', 'ớt sừng'], ARRAY['hot pepper', 'red chili'],
 'spices', 40, 1.9, 8.8, 0.4, true, true, ARRAY[]::TEXT[]),

('650e8400-e29b-41d4-a716-446655440030', 'Ngò rí', 'Cilantro', 'cilantro',
 ARRAY['rau mùi', 'ngò'], ARRAY['coriander', 'Chinese parsley'],
 'herbs', 23, 2.1, 3.7, 0.5, true, true, ARRAY[]::TEXT[]);
```

---

## 3. Users (Test Accounts)

```sql
INSERT INTO users (
    id, email, password_hash, full_name, display_name, avatar_url,
    ai_personality, language, dietary_preferences, allergies,
    is_verified, is_active
) VALUES
-- Admin user
('750e8400-e29b-41d4-a716-446655440001', 
 'admin@cooking.app',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO', -- password: admin123
 'Admin User', 'Admin', 'https://storage.cooking.app/avatars/admin.jpg',
 'professional', 'vi', '[]'::jsonb, '[]'::jsonb,
 true, true),

-- Regular users
('750e8400-e29b-41d4-a716-446655440002',
 'nguyen.van.a@gmail.com',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO', -- password: user123
 'Nguyễn Văn A', 'Chef A', 'https://storage.cooking.app/avatars/user1.jpg',
 'friendly', 'vi', '["vegetarian"]'::jsonb, '["peanuts"]'::jsonb,
 true, true),

('750e8400-e29b-41d4-a716-446655440003',
 'tran.thi.b@gmail.com',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
 'Trần Thị B', 'Home Cook B', 'https://storage.cooking.app/avatars/user2.jpg',
 'humorous', 'vi', '[]'::jsonb, '["shellfish", "dairy"]'::jsonb,
 true, true),

('750e8400-e29b-41d4-a716-446655440004',
 'le.van.c@gmail.com',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
 'Lê Văn C', 'Chef C', 'https://storage.cooking.app/avatars/user3.jpg',
 'nutritionist', 'en', '["vegan", "gluten-free"]'::jsonb, '["gluten"]'::jsonb,
 true, true),

('750e8400-e29b-41d4-a716-446655440005',
 'pham.thi.d@gmail.com',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
 'Phạm Thị D', 'Quick Cook D', 'https://storage.cooking.app/avatars/user4.jpg',
 'efficient', 'vi', '[]'::jsonb, '[]'::jsonb,
 true, true);
```

---

## 4. Recipes (Sample Vietnamese Dishes)

### Recipe 1: Phở Bò Hà Nội

```sql
INSERT INTO recipes (
    id, title_vi, title_en, slug, description_vi, description_en,
    author_id, category_id,
    image_url, thumbnail_url,
    servings, prep_time_minutes, cook_time_minutes,
    difficulty, cuisine, tags, dietary_tags,
    status, published_at, is_featured, rating_average, rating_count
) VALUES (
    '850e8400-e29b-41d4-a716-446655440001',
    'Phở Bò Hà Nội', 
    'Hanoi Beef Pho',
    'pho-bo-ha-noi',
    'Món phở bò truyền thống Hà Nội với nước dùng đậm đà từ xương hầm 12 tiếng. Hương vị đặc trưng từ gừng nướng, hành khô, và ngũ vị hương.',
    'Traditional Hanoi beef pho with rich broth from 12-hour simmered bones. Distinctive flavor from roasted ginger, shallots, and five-spice powder.',
    '750e8400-e29b-41d4-a716-446655440002', -- Nguyễn Văn A
    '550e8400-e29b-41d4-a716-446655440001', -- Main Dishes
    'https://storage.cooking.app/recipes/pho-bo/main.jpg',
    'https://storage.cooking.app/recipes/pho-bo/thumb.jpg',
    4, 30, 720, -- 12 hours cooking
    'hard', 'vietnamese',
    '["traditional", "comfort-food", "popular", "authentic"]'::jsonb,
    '[]'::jsonb,
    'published', CURRENT_TIMESTAMP, true, 4.8, 156
);

-- Recipe Ingredients for Phở Bò
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, ingredient_group, sort_order) VALUES
-- Nước dùng (Broth)
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440001', 2.0, 'kg', 'Nước dùng', 1), -- Xương bò
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440009', 100, 'g', 'Nước dùng', 2), -- Gừng
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440010', 3, 'củ', 'Nước dùng', 3), -- Hành tây
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440022', 2, 'tsp', 'Nước dùng', 4), -- Muối
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440024', 3, 'tbsp', 'Nước dùng', 5), -- Nước mắm

-- Nguyên liệu chính (Main)
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440002', 500, 'g', 'Nguyên liệu chính', 6), -- Thịt bò
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440018', 500, 'g', 'Nguyên liệu chính', 7), -- Bánh phở

-- Rau ăn kèm (Garnish)
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440017', 1, 'bó', 'Rau ăn kèm', 8), -- Hành lá
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440030', 1, 'bó', 'Rau ăn kèm', 9), -- Ngò rí
('850e8400-e29b-41d4-a716-446655440001', '650e8400-e29b-41d4-a716-446655440029', 2, 'trái', 'Rau ăn kèm', 10); -- Ớt

-- Recipe Steps for Phở Bò
INSERT INTO recipe_steps (recipe_id, step_number, title_vi, instructions_vi, has_timer, timer_duration_seconds, timer_name, tip_vi, sort_order) VALUES
('850e8400-e29b-41d4-a716-446655440001', 1, 
 'Chuẩn bị nguyên liệu',
 'Rửa sạch xương bò, ngâm nước muối 30 phút. Gừng nướng thơm, đập dập. Hành tây bỏ vỏ, nướng vàng.',
 true, 1800, 'Ngâm xương',
 'Ngâm xương với nước muối giúp khử mùi hôi và làm trắng xương',
 1),

('850e8400-e29b-41d4-a716-446655440001', 2,
 'Luộc xương sơ chế',
 'Cho xương vào nồi nước sôi, thêm gừng đập dập. Luộc 5 phút rồi vớt ra rửa sạch. Điều này giúp khử mùi hôi xương.',
 true, 300, 'Luộc xương',
 'Nước luộc xương nên đổ đi, không dùng để nấu phở',
 2),

('850e8400-e29b-41d4-a716-446655440001', 3,
 'Hầm nước dùng',
 'Cho xương đã luộc vào nồi nước mới, thêm gừng nướng, hành khô nướng. Đun sôi rồi hạ lửa nhỏ, hầm trong 10-12 tiếng. Hớt bọt trong quá trình hầm.',
 true, 43200, 'Hầm nước dùng', -- 12 hours
 'Hầm càng lâu nước dùng càng ngọt và đậm đà. Không đậy nắp hoàn toàn để tránh nước dùng bị đục',
 3),

('850e8400-e29b-41d4-a716-446655440001', 4,
 'Nêm nếm nước dùng',
 'Sau khi hầm, nêm muối và nước mắm cho vừa ăn. Lọc bỏ xương và rau củ, chỉ giữ lại nước trong.',
 false, null, null,
 'Nêm nếm từ từ, nếm thử nhiều lần để đạt độ vừa miệng',
 4),

('850e8400-e29b-41d4-a716-446655440001', 5,
 'Chuẩn bị thịt và bánh phở',
 'Thịt bò thái lát mỏng. Bánh phở trụng qua nước sôi 1-2 phút cho chín mềm, vớt ra để ráo.',
 true, 120, 'Trụng bánh phở',
 'Thái thịt bò rất mỏng để khi chan nước dùng nóng, thịt sẽ chín vừa đủ',
 5),

('850e8400-e29b-41d4-a716-446655440001', 6,
 'Chuẩn bị rau thơm',
 'Hành lá, ngò rí rửa sạch, thái nhỏ. Ớt thái lát.',
 false, null, null,
 'Rau thơm để riêng, thực khách tự thêm theo khẩu vị',
 6),

('850e8400-e29b-41d4-a716-446655440001', 7,
 'Bày tô phở',
 'Cho bánh phở vào tô, xếp thịt bò thái lên trên. Rắc hành lá, ngò rí.',
 false, null, null,
 null,
 7),

('850e8400-e29b-41d4-a716-446655440001', 8,
 'Hoàn thành',
 'Chan nước dùng nóng lên tô. Ăn kèm rau sống, chanh, ớt tươi.',
 false, null, null,
 'Nước dùng phải đủ nóng để chín tái thịt bò',
 8);

-- Nutrition Facts for Phở Bò
INSERT INTO nutrition_facts (recipe_id, serving_size, calories, protein_g, carbohydrates_g, fat_g, fiber_g, sodium_mg) VALUES
('850e8400-e29b-41d4-a716-446655440001',
 '1 tô (500ml)', 450, 30, 52, 12, 3, 1800);
```

---

### Recipe 2: Cơm Gà Hải Nam

```sql
INSERT INTO recipes (
    id, title_vi, title_en, slug, description_vi, description_en,
    author_id, category_id,
    image_url, thumbnail_url,
    servings, prep_time_minutes, cook_time_minutes,
    difficulty, cuisine, tags, dietary_tags,
    status, published_at, is_featured, rating_average, rating_count
) VALUES (
    '850e8400-e29b-41d4-a716-446655440002',
    'Cơm Gà Hải Nam',
    'Hainanese Chicken Rice',
    'com-ga-hai-nam',
    'Món cơm gà Hải Nam với gà luộc mềm, cơm thơm béo nấu từ mỡ gà. Món ăn đơn giản nhưng cực kỳ ngon và bổ dưỡng.',
    'Hainanese chicken rice with tender poached chicken and fragrant rice cooked in chicken fat. Simple but incredibly delicious.',
    '750e8400-e29b-41d4-a716-446655440003', -- Trần Thị B
    '550e8400-e29b-41d4-a716-446655440001', -- Main Dishes
    'https://storage.cooking.app/recipes/com-ga/main.jpg',
    'https://storage.cooking.app/recipes/com-ga/thumb.jpg',
    4, 20, 45,
    'medium', 'vietnamese',
    '["quick", "healthy", "popular", "one-pot"]'::jsonb,
    '[]'::jsonb,
    'published', CURRENT_TIMESTAMP, true, 4.6, 89
);

-- Recipe Ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, ingredient_group, sort_order) VALUES
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440003', 1, 'con', 'Nguyên liệu chính', 1), -- Gà
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440019', 400, 'g', 'Nguyên liệu chính', 2), -- Gạo
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440009', 50, 'g', 'Gia vị', 3), -- Gừng
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440011', 5, 'tép', 'Gia vị', 4), -- Tỏi
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440022', 1, 'tsp', 'Gia vị', 5), -- Muối
('850e8400-e29b-41d4-a716-446655440002', '650e8400-e29b-41d4-a716-446655440017', 1, 'bó', 'Rau ăn kèm', 6); -- Hành lá

-- Recipe Steps (shortened for brevity)
INSERT INTO recipe_steps (recipe_id, step_number, title_vi, instructions_vi, has_timer, timer_duration_seconds, sort_order) VALUES
('850e8400-e29b-41d4-a716-446655440002', 1, 'Sơ chế gà', 'Gà rửa sạch, chà muối và gừng lên khắp con gà. Để 15 phút.', true, 900, 1),
('850e8400-e29b-41d4-a716-446655440002', 2, 'Luộc gà', 'Luộc gà trong nước sôi với gừng và hành. Luộc 25 phút, vớt ra ngâm nước đá.', true, 1500, 2),
('850e8400-e29b-41d4-a716-446655440002', 3, 'Nấu cơm', 'Phi thơm tỏi, cho gạo vào xào. Thêm nước luộc gà, nấu cơm.', true, 1200, 3),
('850e8400-e29b-41d4-a716-446655440002', 4, 'Hoàn thành', 'Thái gà, bày cơm lên đĩa. Ăn kèm nước chấm và dưa leo.', false, null, 4);
```

---

### Recipe 3: Gỏi Cuốn

```sql
INSERT INTO recipes (
    id, title_vi, title_en, slug, description_vi,
    author_id, category_id,
    image_url, servings, prep_time_minutes, cook_time_minutes,
    difficulty, cuisine, tags, dietary_tags,
    status, published_at, rating_average, rating_count
) VALUES (
    '850e8400-e29b-41d4-a716-446655440003',
    'Gỏi Cuốn Tôm Thịt',
    'Vietnamese Spring Rolls',
    'goi-cuon-tom-thit',
    'Món gỏi cuốn tươi mát với tôm, thịt, rau sống. Ăn kèm nước chấm đậm đà.',
    '750e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440002', -- Appetizers
    'https://storage.cooking.app/recipes/goi-cuon/main.jpg',
    4, 30, 15,
    'easy', 'vietnamese',
    '["quick", "healthy", "fresh", "no-cook"]'::jsonb,
    '[]'::jsonb,
    'published', CURRENT_TIMESTAMP, 4.9, 234
);

-- Ingredients and steps...
```

---

## 5. Ratings & Reviews

```sql
INSERT INTO ratings (user_id, recipe_id, rating, review_text, actual_difficulty, would_cook_again, is_verified_cook) VALUES
('750e8400-e29b-41d4-a716-446655440002', '850e8400-e29b-41d4-a716-446655440001',
 5, 'Phở rất ngon! Nước dùng đậm đà, thơm mùi gừng. Tuy hơi mất thời gian nhưng đáng công.',
 'hard', true, true),

('750e8400-e29b-41d4-a716-446655440003', '850e8400-e29b-41d4-a716-446655440001',
 5, 'Làm theo đúng hướng dẫn, phở ngon như hàng quán. Gia đình ai cũng khen!',
 'medium', true, true),

('750e8400-e29b-41d4-a716-446655440004', '850e8400-e29b-41d4-a716-446655440002',
 5, 'Cơm gà dễ làm, ngon và healthy. Sẽ làm lại nhiều lần.',
 'easy', true, true),

('750e8400-e29b-41d4-a716-446655440005', '850e8400-e29b-41d4-a716-446655440002',
 4, 'Ngon nhưng tôi thấy cơm hơi nhạt. Lần sau sẽ cho thêm gia vị.',
 'medium', true, true);
```

---

## 6. Cooking Sessions (Active)

```sql
INSERT INTO cooking_sessions (
    id, user_id, recipe_id, current_step, total_steps, completed_steps,
    status, started_at, elapsed_time_seconds
) VALUES
('950e8400-e29b-41d4-a716-446655440001',
 '750e8400-e29b-41d4-a716-446655440002',
 '850e8400-e29b-41d4-a716-446655440001',
 5, 8, ARRAY[1, 2, 3, 4],
 'active', CURRENT_TIMESTAMP - INTERVAL '2 hours', 7200);

-- Active timer for the session
INSERT INTO cooking_timers (
    session_id, name, duration_seconds, remaining_seconds, step_number, status
) VALUES
('950e8400-e29b-41d4-a716-446655440001',
 'Hầm nước dùng', 43200, 36000, 3, 'active');
```

---

## 7. Favorites

```sql
INSERT INTO favorites (user_id, recipe_id, personal_note) VALUES
('750e8400-e29b-41d4-a716-446655440002', '850e8400-e29b-41d4-a716-446655440001',
 'Món phở yêu thích của cả nhà. Làm vào cuối tuần.'),
('750e8400-e29b-41d4-a716-446655440002', '850e8400-e29b-41d4-a716-446655440002',
 'Món dễ làm cho bữa trưa'),
('750e8400-e29b-41d4-a716-446655440003', '850e8400-e29b-41d4-a716-446655440001', null),
('750e8400-e29b-41d4-a716-446655440003', '850e8400-e29b-41d4-a716-446655440003', 'Healthy và tươi mát');
```

---

## 8. Search Queries (Recent)

```sql
INSERT INTO search_queries (user_id, query, query_normalized, result_count, clicked_recipe_id) VALUES
('750e8400-e29b-41d4-a716-446655440002', 'phở bò', 'pho bo', 15, '850e8400-e29b-41d4-a716-446655440001'),
('750e8400-e29b-41d4-a716-446655440002', 'món chay', 'mon chay', 32, null),
('750e8400-e29b-41d4-a716-446655440003', 'cơm gà', 'com ga', 8, '850e8400-e29b-41d4-a716-446655440002'),
(NULL, 'bánh mì', 'banh mi', 12, null),
(NULL, 'món ăn sáng', 'mon an sang', 45, null);
```

---

## 9. Trending Keywords

```sql
INSERT INTO trending_keywords (keyword, search_count, trend_score, period) VALUES
('phở', 156, 95.5, 'daily'),
('cơm gà', 89, 78.2, 'daily'),
('gỏi cuốn', 67, 65.8, 'daily'),
('bún chả', 54, 58.3, 'daily'),
('bánh mì', 134, 92.1, 'daily'),
('món chay', 78, 71.4, 'daily'),
('món ăn sáng', 112, 85.7, 'daily'),
('canh chua', 43, 52.6, 'daily');
```

---

## 10. Chat Messages (Sample Conversation)

```sql
-- Create chat
INSERT INTO chats (id, user_id, title, context_type, ai_personality, message_count) VALUES
('a50e8400-e29b-41d4-a716-446655440001',
 '750e8400-e29b-41d4-a716-446655440002',
 'Hỏi về món phở', 'general', 'friendly', 4);

-- Chat messages
INSERT INTO chat_messages (chat_id, role, content) VALUES
('a50e8400-e29b-41d4-a716-446655440001', 'user',
 'Làm thế nào để nước phở trong và ngọt?'),

('a50e8400-e29b-41d4-a716-446655440001', 'assistant',
 'Để có nước phở trong và ngọt, bạn cần chú ý những điểm sau:\n\n1. **Luộc sơ xương**: Luộc xương qua nước sôi 5 phút rồi rửa sạch để loại bỏ tạp chất\n2. **Hầm nhỏ lửa**: Duy trì lửa nhỏ, không sôi mạnh để nước không bị đục\n3. **Hớt bọt thường xuyên**: Trong 2 giờ đầu, hớt bọt mỗi 15-20 phút\n4. **Không đậy kín nắp**: Để hơi thoát ra, tránh nước bị đục\n5. **Nướng gừng và hành**: Gừng và hành khô nướng thơm sẽ tăng hương vị ngọt tự nhiên\n\nMột mẹo nhỏ: Có thể thêm 1-2 củ cà rốt hoặc củ cải trắng khi hầm để tăng độ ngọt tự nhiên nhé! 😊'),

('a50e8400-e29b-41d4-a716-446655440001', 'user',
 'Hầm bao lâu là đủ?'),

('a50e8400-e29b-41d4-a716-446655440001', 'assistant',
 'Thời gian hầm tùy thuộc vào loại xương và độ đậm đà bạn muốn:\n\n**Tối thiểu:** 4-6 giờ cho nước dùng đủ vị\n**Chuẩn:** 8-10 giờ cho nước dùng đậm đà, thơm ngon\n**Tốt nhất:** 12-14 giờ cho nước dùng cô đặc, ngọt tự nhiên\n\nMẹo: Nhiều quán phở Hà Nội nổi tiếng hầm 14-16 giờ! Nếu bạn có instant pot/nồi áp suất, có thể rút ngắn xuống 3-4 giờ nhưng vị sẽ khác một chút.\n\nBạn có muốn xem công thức phở bò Hà Nội chi tiết không? 🍜');
```

---

## Python Script to Import Data

```python
# scripts/seed_database.py
import asyncio
import asyncpg
from datetime import datetime
import json

async def seed_database():
    """Seed database with sample data"""
    
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='your_password',
        database='cooking_assistant'
    )
    
    print("Connected to database")
    
    # Read SQL file
    with open('sample_data.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Execute
    await conn.execute(sql_content)
    
    print("✅ Database seeded successfully!")
    
    # Verify
    count = await conn.fetchval('SELECT COUNT(*) FROM recipes')
    print(f"Total recipes: {count}")
    
    await conn.close()

if __name__ == '__main__':
    asyncio.run(seed_database())
```

---

## Summary

### Data Statistics

```
Categories:           15 items
Ingredients:          30 items (expandable to 500+)
Users:                5 test accounts
Recipes:              3 complete recipes (expandable)
Recipe Steps:         20 steps total
Ratings:              4 reviews
Favorites:            4 saved recipes
Cooking Sessions:     1 active session
Search Queries:       5 recent searches
Trending Keywords:    8 keywords
Chat Messages:        4 messages (1 conversation)
```

### File Structure

```
docs/backend/
├── 01-database-schema.md
└── 02-sample-data.md  (this file)

scripts/
├── seed_database.py
└── sample_data.sql
```

---

**✅ Sample Data Complete!**

Tất cả format data cần thiết để seed database đã được chuẩn bị:
- ✅ SQL INSERT statements (ready to execute)
- ✅ JSON format (for API imports)
- ✅ Python seeding script
- ✅ Complete Vietnamese recipes with ingredients, steps, timers
- ✅ Test user accounts
- ✅ Sample ratings, favorites, cooking sessions
- ✅ Chat conversation examples

Data này có thể expand dễ dàng cho production! 🚀
