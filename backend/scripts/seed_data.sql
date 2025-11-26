-- Database Seed Data
-- Generated from JSON files
-- Run with: Get-Content seed_data.sql | docker exec -i cooking_assistant_db psql -U cooking_admin -d cooking_assistant

-- Disable triggers for faster bulk insert
SET session_replication_role = 'replica';


-- Insert categories

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440001', 'Món chính', 'Main Dishes', 'main-dishes',
        'Các món ăn chính trong bữa cơm', 'Main courses and entrees',
        'https://storage.cooking.app/icons/main-dishes.svg', 'https://storage.cooking.app/categories/main-dishes.jpg',
        1, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440002', 'Món khai vị', 'Appetizers', 'appetizers',
        'Món ăn khai vị, món nhắm', 'Starters and small plates',
        'https://storage.cooking.app/icons/appetizers.svg', 'https://storage.cooking.app/categories/appetizers.jpg',
        2, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440003', 'Món tráng miệng', 'Desserts', 'desserts',
        'Món ngọt, bánh, tráng miệng', 'Sweet dishes and desserts',
        'https://storage.cooking.app/icons/desserts.svg', 'https://storage.cooking.app/categories/desserts.jpg',
        3, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440004', 'Món súp', 'Soups', 'soups',
        'Các loại súp, canh, lẩu', 'Soups and broths',
        'https://storage.cooking.app/icons/soups.svg', 'https://storage.cooking.app/categories/soups.jpg',
        4, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440005', 'Đồ uống', 'Beverages', 'beverages',
        'Nước uống, sinh tố, cocktail', 'Drinks and beverages',
        'https://storage.cooking.app/icons/beverages.svg', 'https://storage.cooking.app/categories/beverages.jpg',
        5, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440006', 'Món ăn sáng', 'Breakfast', 'breakfast',
        'Món ăn sáng, brunch', 'Breakfast and brunch dishes',
        'https://storage.cooking.app/icons/breakfast.svg', 'https://storage.cooking.app/categories/breakfast.jpg',
        6, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440007', 'Món salad', 'Salads', 'salads',
        'Salad rau củ, trộn', 'Fresh salads',
        'https://storage.cooking.app/icons/salads.svg', 'https://storage.cooking.app/categories/salads.jpg',
        7, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440008', 'Món nướng', 'Grilled', 'grilled',
        'Món nướng, BBQ', 'Grilled and barbecue',
        'https://storage.cooking.app/icons/grilled.svg', 'https://storage.cooking.app/categories/grilled.jpg',
        8, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440009', 'Món chiên', 'Fried', 'fried',
        'Món chiên giòn, rán', 'Fried dishes',
        'https://storage.cooking.app/icons/fried.svg', 'https://storage.cooking.app/categories/fried.jpg',
        9, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440010', 'Món hấp', 'Steamed', 'steamed',
        'Món hấp, dim sum', 'Steamed dishes',
        'https://storage.cooking.app/icons/steamed.svg', 'https://storage.cooking.app/categories/steamed.jpg',
        10, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440011', 'Món xào', 'Stir-fried', 'stir-fried',
        'Món xào, rim', 'Stir-fried dishes',
        'https://storage.cooking.app/icons/stir-fried.svg', 'https://storage.cooking.app/categories/stir-fried.jpg',
        11, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440012', 'Món hầm', 'Braised', 'braised',
        'Món hầm, kho, om', 'Braised and stewed',
        'https://storage.cooking.app/icons/braised.svg', 'https://storage.cooking.app/categories/braised.jpg',
        12, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440013', 'Bánh mì & Sandwich', 'Bread & Sandwiches', 'bread-sandwiches',
        'Bánh mì, sandwich các loại', 'Breads and sandwiches',
        'https://storage.cooking.app/icons/bread.svg', 'https://storage.cooking.app/categories/bread.jpg',
        13, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440014', 'Món chay', 'Vegetarian', 'vegetarian',
        'Món ăn chay, thuần chay', 'Vegetarian and vegan',
        'https://storage.cooking.app/icons/vegetarian.svg', 'https://storage.cooking.app/categories/vegetarian.jpg',
        14, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO categories (id, name_vi, name_en, slug, description_vi, description_en, icon_url, image_url, display_order, is_active)
VALUES ('550e8400-e29b-41d4-a716-446655440015', 'Món Việt', 'Vietnamese', 'vietnamese',
        'Món ăn Việt Nam truyền thống', 'Traditional Vietnamese cuisine',
        'https://storage.cooking.app/icons/vietnamese.svg', 'https://storage.cooking.app/categories/vietnamese.jpg',
        15, true)
ON CONFLICT (id) DO NOTHING;



-- Insert users

INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('750e8400-e29b-41d4-a716-446655440001', 'admin@cooking.app', NULL,
        'Admin User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
        'https://storage.cooking.app/avatars/admin.jpg', 'user',
        true, false,
        'professional', ARRAY[]::text[], ARRAY[]::text[],
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('750e8400-e29b-41d4-a716-446655440002', 'nguyen.van.a@gmail.com', NULL,
        'Nguyễn Văn A', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
        'https://storage.cooking.app/avatars/user1.jpg', 'user',
        true, false,
        'friendly', ARRAY['vegetarian']::text[], ARRAY['peanuts']::text[],
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('750e8400-e29b-41d4-a716-446655440003', 'tran.thi.b@gmail.com', NULL,
        'Trần Thị B', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
        'https://storage.cooking.app/avatars/user2.jpg', 'user',
        true, false,
        'humorous', ARRAY[]::text[], ARRAY['shellfish','dairy']::text[],
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('750e8400-e29b-41d4-a716-446655440004', 'le.van.c@gmail.com', NULL,
        'Lê Văn C', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
        'https://storage.cooking.app/avatars/user3.jpg', 'user',
        true, false,
        'nutritionist', ARRAY['vegan','gluten-free']::text[], ARRAY['gluten']::text[],
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, email, username, full_name, password_hash, avatar_url, role, is_active, is_email_verified, ai_personality, dietary_preferences, allergies, cooking_skill_level, preferred_cuisines)
VALUES ('750e8400-e29b-41d4-a716-446655440005', 'pham.thi.d@gmail.com', NULL,
        'Phạm Thị D', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Zy1HlvQ6JmFO',
        'https://storage.cooking.app/avatars/user4.jpg', 'user',
        true, false,
        'efficient', ARRAY[]::text[], ARRAY[]::text[],
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;



-- Insert ingredients

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440001', 'Xương bò', 'Beef bones', 'beef-bones',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/beef-bones.jpg', NULL,
        NULL,
        20,
        NULL,
        8,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440002', 'Thịt bò', 'Beef', 'beef',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/beef.jpg', NULL,
        NULL,
        26,
        NULL,
        15,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440003', 'Thịt gà', 'Chicken', 'chicken',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/chicken.jpg', NULL,
        NULL,
        31,
        NULL,
        3.6,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440004', 'Thịt heo', 'Pork', 'pork',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/pork.jpg', NULL,
        NULL,
        27,
        NULL,
        14,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440005', 'Tôm', 'Shrimp', 'shrimp',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/shrimp.jpg', NULL,
        NULL,
        24,
        0.2,
        0.3,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440006', 'Cá', 'Fish', 'fish',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/fish.jpg', NULL,
        NULL,
        26,
        NULL,
        2.8,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440007', 'Trứng gà', 'Chicken eggs', 'eggs',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/eggs.jpg', NULL,
        NULL,
        13,
        1.1,
        11,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440008', 'Đậu phụ', 'Tofu', 'tofu',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/tofu.jpg', NULL,
        NULL,
        8,
        1.9,
        4.8,
        0.3,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440009', 'Gừng', 'Ginger', 'ginger',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/ginger.jpg', NULL,
        NULL,
        1.8,
        18,
        0.8,
        2,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440010', 'Hành tây', 'Onion', 'onion',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/onion.jpg', NULL,
        NULL,
        1.1,
        9.3,
        0.1,
        1.7,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440011', 'Tỏi', 'Garlic', 'garlic',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/garlic.jpg', NULL,
        NULL,
        6.4,
        33,
        0.5,
        2.1,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440012', 'Cà chua', 'Tomato', 'tomato',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/tomato.jpg', NULL,
        NULL,
        0.9,
        3.9,
        0.2,
        1.2,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440013', 'Cà rốt', 'Carrot', 'carrot',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/carrot.jpg', NULL,
        NULL,
        0.9,
        10,
        0.2,
        2.8,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440014', 'Khoai tây', 'Potato', 'potato',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/potato.jpg', NULL,
        NULL,
        2,
        17,
        0.1,
        2.2,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440015', 'Rau muống', 'Water spinach', 'water-spinach',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/water-spinach.jpg', NULL,
        NULL,
        2.6,
        2.1,
        0.2,
        2.1,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440016', 'Rau ngót', 'Sweet leaf', 'sweet-leaf',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/sweet-leaf.jpg', NULL,
        NULL,
        4.8,
        6.3,
        0.5,
        3.1,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440017', 'Hành lá', 'Spring onion', 'spring-onion',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/spring-onion.jpg', NULL,
        NULL,
        1.8,
        7.3,
        0.2,
        2.6,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440018', 'Bánh phở', 'Pho noodles', 'pho-noodles',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/pho-noodles.jpg', NULL,
        NULL,
        1.8,
        25,
        0.2,
        1.2,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440019', 'Gạo', 'Rice', 'rice',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/rice.jpg', NULL,
        NULL,
        2.7,
        28,
        0.3,
        0.4,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440020', 'Bún', 'Rice vermicelli', 'rice-vermicelli',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/vermicelli.jpg', NULL,
        NULL,
        1.8,
        24,
        0.1,
        1,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440021', 'Mì', 'Wheat noodles', 'wheat-noodles',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/noodles.jpg', NULL,
        NULL,
        4.5,
        25,
        2.1,
        1.2,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440022', 'Muối', 'Salt', 'salt',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/salt.jpg', NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440023', 'Đường', 'Sugar', 'sugar',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/sugar.jpg', NULL,
        NULL,
        NULL,
        100,
        NULL,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440024', 'Nước mắm', 'Fish sauce', 'fish-sauce',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/fish-sauce.jpg', NULL,
        NULL,
        5.5,
        3.5,
        NULL,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440025', 'Dầu ăn', 'Cooking oil', 'cooking-oil',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/oil.jpg', NULL,
        NULL,
        NULL,
        NULL,
        100,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440026', 'Xì dầu', 'Soy sauce', 'soy-sauce',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/soy-sauce.jpg', NULL,
        NULL,
        5.5,
        4.9,
        0.1,
        0.8,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440027', 'Hạt nêm', 'Seasoning powder', 'seasoning-powder',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/seasoning.jpg', NULL,
        NULL,
        5,
        15,
        NULL,
        NULL,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440028', 'Tiêu', 'Black pepper', 'black-pepper',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/pepper.jpg', NULL,
        NULL,
        10.4,
        64,
        3.3,
        25.3,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440029', 'Ớt', 'Chili pepper', 'chili',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/chili.jpg', NULL,
        NULL,
        1.9,
        8.8,
        0.4,
        1.5,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;

INSERT INTO ingredients (id, name_vi, name_en, slug, description_vi, description_en, image_url, category_id, calories_per_100g, protein_g, carbs_g, fat_g, fiber_g, common_unit, allergen_types)
VALUES ('650e8400-e29b-41d4-a716-446655440030', 'Ngò rí', 'Cilantro', 'cilantro',
        NULL, NULL,
        'https://storage.cooking.app/ingredients/cilantro.jpg', NULL,
        NULL,
        2.1,
        3.7,
        0.5,
        2.8,
        NULL, ARRAY[]::text[])
ON CONFLICT (id) DO NOTHING;



-- Insert recipes

INSERT INTO recipes (id, title_vi, title_en, slug, description_vi, description_en, author_id, category_id, prep_time_minutes, cook_time_minutes, total_time_minutes, servings, difficulty, thumbnail_url, video_url, is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, allergens, is_published, is_featured)
VALUES ('850e8400-e29b-41d4-a716-446655440001', 'Phở Bò Hà Nội', 'Hanoi Beef Pho', 'pho-bo-ha-noi',
        'Món phở bò truyền thống Hà Nội với nước dùng thơm ngon, được hầm từ xương bò trong nhiều giờ. Kèm theo thịt bò tái, chín và các loại rau thơm đặc trưng.', 'Traditional Hanoi beef pho with aromatic broth simmered from beef bones for many hours. Served with rare and cooked beef slices and fresh herbs.',
        '750e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440015',
        30,
        720,
        750,
        4, 'hard',
        NULL, 'https://storage.cooking.app/videos/pho-bo-tutorial.mp4',
        false, false,
        true, true,
        ARRAY[]::text[], true, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipes (id, title_vi, title_en, slug, description_vi, description_en, author_id, category_id, prep_time_minutes, cook_time_minutes, total_time_minutes, servings, difficulty, thumbnail_url, video_url, is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, allergens, is_published, is_featured)
VALUES ('850e8400-e29b-41d4-a716-446655440002', 'Cơm Gà Hải Nam', 'Hainanese Chicken Rice', 'com-ga-hai-nam',
        'Món cơm gà Hải Nam với thịt gà luộc mềm, cơm thơm béo nấu với nước luộc gà và mỡ gà. Ăn kèm nước sốt gừng và tương ớt.', 'Hainanese chicken rice with tender poached chicken, fragrant rice cooked in chicken broth and fat. Served with ginger sauce and chili sauce.',
        '750e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440001',
        15,
        45,
        60,
        4, 'medium',
        NULL, NULL,
        false, false,
        true, true,
        ARRAY[]::text[], true, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipes (id, title_vi, title_en, slug, description_vi, description_en, author_id, category_id, prep_time_minutes, cook_time_minutes, total_time_minutes, servings, difficulty, thumbnail_url, video_url, is_vegetarian, is_vegan, is_gluten_free, is_dairy_free, allergens, is_published, is_featured)
VALUES ('850e8400-e29b-41d4-a716-446655440003', 'Gỏi Cuốn Tôm Thịt', 'Vietnamese Spring Rolls', 'goi-cuon-tom-thit',
        'Gỏi cuốn tươi ngon với tôm, thịt heo luộc, bún tươi và rau thơm đặc trưng. Ăn kèm nước chấm chua ngọt.', 'Fresh spring rolls with shrimp, boiled pork, vermicelli noodles and fresh herbs. Served with sweet and sour dipping sauce.',
        '750e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002',
        25,
        15,
        40,
        4, 'easy',
        NULL, 'https://storage.cooking.app/videos/goi-cuon-tutorial.mp4',
        false, false,
        true, true,
        ARRAY['shellfish']::text[], true, true)
ON CONFLICT (id) DO NOTHING;


-- Re-enable triggers
SET session_replication_role = 'origin';

-- Update sequences
SELECT setval(pg_get_serial_sequence('categories', 'id'), (SELECT MAX(id) FROM categories));

-- Verify data
SELECT 'Categories' as table_name, COUNT(*) as count FROM categories
UNION ALL SELECT 'Users', COUNT(*) FROM users
UNION ALL SELECT 'Ingredients', COUNT(*) FROM ingredients
UNION ALL SELECT 'Recipes', COUNT(*) FROM recipes;

DO $$
BEGIN
    RAISE NOTICE 'Database seeding completed successfully!';
END $$;