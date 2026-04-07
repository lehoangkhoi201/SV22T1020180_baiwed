# EzLuyenThi — Schema `public` (từ PostgREST OpenAPI)

Nguồn: `ezluyenthi_openapi_snapshot.json` — `standard public schema`.

Đây là **cấu trúc bảng/cột** mà PostgREST công khai qua **anon key** (giống client).
**Không** gồm: policy RLS, trigger, view không expose, index, quyền chi tiết — xem thêm trong Supabase SQL Editor nếu cần.

---

## `ai_analysis`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `analysis_data` | `jsonb` | có |  |
| `analysis_type` | `string` / `character varying` |  | default: `exam_result` |
| `attempt_id` | `string` / `uuid` |  | FK → `exam_attempts.id` |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `exam_id` | `string` / `uuid` |  | FK → `exams.id` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `model_used` | `string` / `character varying` |  | default: `llama-3.3-70b-versatile` |
| `tokens_used` | `integer` / `integer` |  | default: `0` |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `allowed_origins`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `origin` | `string` / `text` | có |  |

## `app_settings`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `key` | `string` / `text` |  |  |
| `value` | `string` / `text` |  |  |
| `visibility` | `string` / `text` |  |  |

## `battle_queue`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `difficulty` | `string` / `text` | có | default: `medium` |
| `elo_rating` | `integer` / `integer` |  | default: `1000` |
| `expires_at` | `string` / `timestamp with time zone` | có | default: `(now() + '00:05:00'::interval)` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `language_id` | `string` / `uuid` | có | FK → `programming_languages.id` |
| `user_id` | `string` / `uuid` | có |  |

## `battle_submissions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `ai_feedback` | `string` / `text` |  |  |
| `battle_id` | `string` / `uuid` | có | FK → `battles.id` |
| `code_encrypted` | `string` / `text` | có |  |
| `error_message` | `string` / `text` |  |  |
| `execution_time_ms` | `integer` / `integer` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `judged_at` | `string` / `timestamp with time zone` |  |  |
| `language_id` | `string` / `uuid` | có | FK → `programming_languages.id` |
| `memory_used_mb` | `number` / `numeric` |  |  |
| `score` | `integer` / `integer` |  | default: `0` |
| `status` | `string` / `text` | có |  |
| `submitted_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `test_cases_passed` | `integer` / `integer` |  | default: `0` |
| `test_cases_total` | `integer` / `integer` |  | default: `0` |
| `test_results` | `jsonb` |  |  |
| `user_id` | `string` / `uuid` | có |  |

## `battle_templates`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `challenge_data` | `jsonb` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `description` | `string` / `text` | có |  |
| `difficulty` | `string` / `text` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `language_id` | `string` / `uuid` | có | FK → `programming_languages.id` |
| `times_used` | `integer` / `integer` |  | default: `0` |
| `title` | `string` / `text` | có |  |

## `battles`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `challenge_id` | `string` / `uuid` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `difficulty` | `string` / `text` | có | default: `medium` |
| `ended_at` | `string` / `timestamp with time zone` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `language_id` | `string` / `uuid` | có | FK → `programming_languages.id` |
| `player1_elo_after` | `integer` / `integer` |  |  |
| `player1_elo_before` | `integer` / `integer` |  |  |
| `player1_elo_change` | `integer` / `integer` |  | default: `0` |
| `player1_id` | `string` / `uuid` | có |  |
| `player1_score` | `integer` / `integer` |  | default: `0` |
| `player1_submission_time_ms` | `integer` / `integer` |  |  |
| `player2_elo_after` | `integer` / `integer` |  |  |
| `player2_elo_before` | `integer` / `integer` |  |  |
| `player2_elo_change` | `integer` / `integer` |  | default: `0` |
| `player2_id` | `string` / `uuid` |  |  |
| `player2_score` | `integer` / `integer` |  | default: `0` |
| `player2_submission_time_ms` | `integer` / `integer` |  |  |
| `result` | `string` / `public.battle_result` |  |  |
| `started_at` | `string` / `timestamp with time zone` |  |  |
| `status` | `string` / `public.battle_status` | có | default: `waiting` |
| `time_limit_seconds` | `integer` / `integer` |  | default: `180` |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `now()` |

## `blog_media`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `media_type` | `string` / `public.media_type` | có |  |
| `media_url` | `string` / `text` | có |  |
| `post_id` | `string` / `uuid` |  | FK → `blog_posts.id` |

## `blog_posts`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `author_id` | `string` / `uuid` |  |  |
| `content` | `string` / `text` | có |  |
| `cover_url` | `string` / `text` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `published_at` | `string` / `timestamp with time zone` |  |  |
| `slug` | `string` / `text` | có |  |
| `status` | `string` / `public.post_status` |  | default: `draft` |
| `title` | `string` / `text` | có |  |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |

## `code_battle_questions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `description` | `string` / `text` | có |  |
| `difficulty` | `string` / `text` |  | default: `medium` |
| `hints` | `jsonb` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `points` | `integer` / `integer` |  | default: `10` |
| `solution_code` | `string` / `text` |  |  |
| `starter_code` | `string` / `text` |  |  |
| `subject_id` | `string` / `uuid` | có | FK → `code_battle_subjects.id` |
| `template_code` | `string` / `text` | có |  |
| `test_cases` | `jsonb` |  |  |
| `time_limit_seconds` | `integer` / `integer` |  | default: `300` |
| `title` | `string` / `text` | có |  |

## `code_battle_subjects`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `color` | `string` / `text` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `icon` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `name` | `string` / `text` | có |  |
| `slug` | `string` / `text` | có |  |

## `code_battle_submissions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `ai_feedback` | `jsonb` |  |  |
| `battle_id` | `string` / `uuid` | có |  |
| `code` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `execution_result` | `jsonb` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `language` | `string` / `text` | có |  |
| `question_id` | `string` / `uuid` | có | FK → `code_battle_questions.id` |
| `score` | `integer` / `integer` |  |  |
| `status` | `string` / `text` |  | default: `pending` |
| `submission_time` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `code_reviews`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `code_content` | `string` / `text` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `feedback` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `language` | `string` / `text` |  |  |
| `problem_url` | `string` / `text` |  |  |
| `score` | `integer` / `integer` |  |  |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` |  |  |

## `commissions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `amount` | `number` / `numeric` | có |  |
| `collaborator_id` | `string` / `uuid` | có | FK → `profiles.id` |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `description` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `order_id` | `string` / `uuid` |  | FK → `wallet_transactions.id` |

## `contact_requests`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `email` | `string` / `text` | có |  |
| `full_name` | `string` / `text` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `interested_course` | `string` / `text` | có |  |
| `message` | `string` / `text` |  |  |
| `phone_number` | `string` / `text` | có |  |
| `user_role` | `string` / `text` |  |  |

## `conversations`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `title` | `string` / `text` | có | default: `New chat` |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `course_purchases`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `amount_paid` | `integer` / `integer` | có | default: `0` |
| `coupon_used` | `string` / `text` |  |  |
| `course_id` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `user_id` | `string` / `uuid` |  | FK → `profiles.id` |

## `exam_attempts`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `answers` | `jsonb` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `exam_id` | `string` / `uuid` |  | FK → `exams.id` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `score` | `number` / `numeric` |  |  |
| `status` | `string` / `character varying` |  | default: `in_progress` |
| `time_spent` | `integer` / `integer` |  |  |
| `user_id` | `string` / `uuid` |  |  |

## `exam_purchases`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `amount` | `number` / `numeric` |  |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `metadata` | `jsonb` |  |  |
| `payment_code` | `string` / `text` | có |  |
| `status` | `string` / `text` |  | default: `pending` |
| `transaction_id` | `string` / `text` |  |  |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `user_id` | `string` / `uuid` |  |  |

## `exam_results`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `completed_at` | `string` / `timestamp with time zone` |  | default: `timezone('utc'::text, now())` |
| `correct_answers` | `integer` / `integer` |  |  |
| `exam_id` | `string` / `uuid` |  | FK → `exams.id` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `score` | `number` / `double precision` |  |  |
| `total_questions` | `integer` / `integer` |  |  |
| `user_id` | `string` / `uuid` |  |  |

## `exam_sessions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `final_quiz_data` | `jsonb` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `image_assignments` | `jsonb` |  |  |
| `images_metadata` | `jsonb` |  |  |
| `original_file_url` | `string` / `text` |  |  |
| `pasted_json` | `jsonb` |  |  |
| `status` | `string` / `text` |  | default: `processing` |
| `title` | `string` / `text` |  | default: `Untitled Exam` |
| `user_id` | `string` / `uuid` | có |  |

## `exams`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `content` | `jsonb` | có |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `timezone('utc'::text, now())` |
| `created_by` | `string` / `uuid` |  |  |
| `description` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `is_ai_generated` | `boolean` / `boolean` |  | default: `False` |
| `is_public` | `boolean` / `boolean` |  | default: `False` |
| `settings` | `jsonb` |  |  |
| `subject` | `string` / `text` |  |  |
| `title` | `string` / `text` | có |  |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |

## `fpt_solver_purchases`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `language` | `string` / `text` | có |  |
| `price_paid` | `integer` / `integer` | có |  |
| `user_id` | `string` / `uuid` | có |  |
| `voucher_used` | `string` / `text` |  |  |

## `ielts_trials`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `skill_id` | `string` / `text` | có | PK |
| `used_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có | PK |

## `leaked_passwords`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `detected_at` | `string` / `timestamp with time zone` |  |  |
| `leak_source` | `string` / `text` |  |  |
| `password_hash` | `string` / `text` |  |  |

## `learning_roadmap`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `completed_tasks` | `jsonb` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `current_week` | `integer` / `integer` |  | default: `1` |
| `difficulty_level` | `string` / `character varying` |  | default: `intermediate` |
| `goal` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `model_used` | `string` / `character varying` |  | default: `llama-3.3-70b-versatile` |
| `progress_percentage` | `number` / `numeric` |  | default: `0.0` |
| `roadmap_data` | `jsonb` | có |  |
| `status` | `string` / `character varying` |  | default: `active` |
| `target_date` | `string` / `date` |  |  |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `library_resources`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `category` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `description` | `string` / `text` |  |  |
| `featured` | `boolean` / `boolean` |  | default: `False` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `link` | `string` / `text` |  |  |
| `title` | `string` / `text` | có |  |
| `type` | `string` / `text` |  |  |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |

## `mentor_applications`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `available_time` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `cv_url` | `string` / `text` |  |  |
| `email` | `string` / `text` | có |  |
| `facebook` | `string` / `text` |  |  |
| `full_name` | `string` / `text` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `motivation` | `string` / `text` | có |  |
| `phone` | `string` / `text` | có |  |
| `skills` | `string` / `text` | có |  |
| `status` | `string` / `text` | có | default: `pending` |
| `subjects` | `string` / `text` | có |  |
| `teaching_experience` | `string` / `text` | có |  |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `user_id` | `string` / `uuid` |  |  |
| `video_url` | `string` / `text` |  |  |
| `work_experience` | `string` / `text` | có |  |

## `messages`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `content` | `string` / `text` | có |  |
| `conversation_id` | `string` / `uuid` | có | FK → `conversations.id` |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `model` | `string` / `text` |  |  |
| `role` | `string` / `text` | có |  |
| `user_id` | `string` / `uuid` | có |  |

## `notifications`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `body` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `created_by` | `string` / `uuid` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_global` | `boolean` / `boolean` |  | default: `False` |
| `link` | `string` / `text` |  |  |
| `title` | `string` / `text` | có |  |
| `type` | `string` / `public.notification_type` | có | default: `system` |
| `user_id` | `string` / `uuid` |  |  |

## `payments`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `amount` | `number` / `numeric` |  |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `timezone('utc'::text, now())` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `status` | `string` / `text` |  |  |
| `transaction_id` | `string` / `text` |  |  |
| `user_id` | `string` / `uuid` |  |  |

## `profiles`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `avatar_url` | `string` / `text` |  |  |
| `battle_elo_rating` | `integer` / `integer` |  | default: `1000` |
| `commission_balance` | `number` / `numeric` |  | default: `0` |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `current_streak` | `integer` / `integer` |  | default: `0` |
| `email` | `string` / `text` | có |  |
| `free_usage_count` | `integer` / `integer` |  | default: `0` |
| `free_usage_limit` | `integer` / `integer` |  | default: `10` |
| `full_name` | `string` / `text` |  |  |
| `grade` | `string` / `text` |  |  |
| `grading_turns` | `integer` / `integer` |  | default: `0` |
| `id` | `string` / `uuid` | có | PK |
| `is_pro` | `boolean` / `boolean` |  | default: `False` |
| `last_check_in` | `string` / `date` |  |  |
| `last_login` | `string` / `timestamp with time zone` |  |  |
| `last_used_at` | `string` / `timestamp with time zone` |  |  |
| `longest_streak` | `integer` / `integer` |  | default: `0` |
| `pro_expires_at` | `string` / `timestamp with time zone` |  |  |
| `rank` | `string` / `text` |  | default: `Unranked` |
| `rank_level` | `string` / `text` |  | default: `Đồng V` |
| `referral_code` | `string` / `text` |  |  |
| `registration_ip` | `string` / `text` |  |  |
| `role` | `string` / `text` | có | default: `user` |
| `stars` | `integer` / `integer` |  | default: `0` |
| `study_goal_reminder_enabled` | `boolean` / `boolean` |  | default: `True` |
| `study_hours` | `number` / `double precision` |  | default: `0` |
| `subjects` | `array` / `text[]` |  |  |
| `total_check_ins` | `integer` / `integer` |  | default: `0` |
| `total_earnings` | `number` / `numeric` |  | default: `0` |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `wallet_balance` | `integer` / `bigint` |  | default: `0` |

## `programming_languages`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `file_extension` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `judge_enabled` | `boolean` / `boolean` |  | default: `True` |
| `monaco_language` | `string` / `text` |  |  |
| `name` | `string` / `text` | có |  |
| `slug` | `string` / `text` | có |  |
| `version` | `string` / `text` |  |  |

## `questions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `correct_answer` | `integer` / `integer` |  | default: `0` |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `exam_id` | `string` / `uuid` | có | FK → `exams.id` |
| `explanation` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `options` | `jsonb` |  |  |
| `order_index` | `integer` / `integer` |  | default: `0` |
| `question_text` | `string` / `text` | có |  |

## `quiz_questions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `code_snippet` | `string` / `text` |  |  |
| `correct_answer_index` | `integer` / `integer` |  |  |
| `course_code` | `string` / `text` |  |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `difficulty` | `string` / `text` |  | default: `medium` |
| `explanation` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `options` | `jsonb` | có |  |
| `question_text` | `string` / `text` | có |  |
| `subject_code` | `string` / `text` | có |  |
| `topic` | `string` / `text` |  |  |

## `referrals`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `referred_user_id` | `string` / `uuid` | có | FK → `profiles.id` |
| `referrer_id` | `string` / `uuid` | có | FK → `profiles.id` |
| `status` | `string` / `text` | có | default: `pending` |

## `reviews`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `comment` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `rating` | `integer` / `smallint` | có |  |
| `user_id` | `string` / `uuid` |  | default: `auth.uid()` |
| `user_name` | `string` / `text` |  |  |

## `saved_exams`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `exam_id` | `string` / `uuid` | có | FK → `exams.id` |
| `folder` | `string` / `character varying` |  | default: `default` |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `notes` | `string` / `text` |  |  |
| `tags` | `array` / `text[]` |  |  |
| `user_id` | `string` / `uuid` | có |  |

## `speaking_sessions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `audio_duration_sec` | `integer` / `integer` |  |  |
| `audio_path` | `string` / `text` |  |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `error_message` | `string` / `text` |  |  |
| `examiner_json` | `jsonb` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `level` | `string` / `text` | có |  |
| `model_used` | `string` / `text` |  |  |
| `processing_time_ms` | `integer` / `integer` |  |  |
| `retry_count` | `integer` / `integer` |  | default: `0` |
| `status` | `string` / `text` | có | default: `created` |
| `topic_id` | `string` / `text` | có |  |
| `topic_name` | `string` / `text` | có |  |
| `transcript_confidence` | `string` / `text` |  |  |
| `transcript_text` | `string` / `text` |  |  |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `subscriptions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `activated_at` | `string` / `timestamp with time zone` |  |  |
| `amount` | `number` / `numeric` |  | default: `0` |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `end_date` | `string` / `timestamp with time zone` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `plan` | `string` / `text` |  | default: `free` |
| `plan_type` | `string` / `text` | có |  |
| `start_date` | `string` / `timestamp with time zone` |  | default: `now()` |
| `status` | `string` / `text` |  | default: `active` |
| `transaction_id_encrypted` | `string` / `text` |  |  |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có |  |

## `toeic_parts`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `part_number` | `integer` / `integer` | có |  |
| `test_id` | `string` / `uuid` |  | FK → `toeic_tests.id` |
| `title` | `string` / `text` |  |  |

## `toeic_question_groups`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `audio_url` | `string` / `text` |  |  |
| `group_order` | `integer` / `integer` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `image_url` | `string` / `text` |  |  |
| `part_id` | `string` / `uuid` |  | FK → `toeic_parts.id` |
| `passage_text` | `string` / `text` |  |  |
| `transcript` | `string` / `text` |  |  |
| `translation` | `string` / `text` |  |  |

## `toeic_questions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `correct_answer` | `integer` / `integer` | có |  |
| `explanation` | `string` / `text` |  |  |
| `group_id` | `string` / `uuid` |  | FK → `toeic_question_groups.id` |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `options` | `jsonb` | có |  |
| `question_number` | `integer` / `integer` | có |  |
| `question_text` | `string` / `text` |  |  |

## `toeic_tests`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `is_pro` | `boolean` / `boolean` |  | default: `False` |
| `title` | `string` / `text` | có |  |
| `total_questions` | `integer` / `integer` |  | default: `200` |
| `year` | `integer` / `integer` |  |  |

## `usage_tracking`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `feature_name` | `string` / `text` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `last_used` | `string` / `timestamp with time zone` |  | default: `now()` |
| `usage_count` | `integer` / `integer` |  | default: `0` |
| `user_id` | `string` / `uuid` | có |  |

## `user_activity`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `activity_data` | `jsonb` |  |  |
| `activity_type` | `string` / `text` | có |  |
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `user_id` | `string` / `uuid` | có |  |

## `user_login_streaks`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `current_streak` | `integer` / `integer` |  | default: `0` |
| `last_claim_at` | `string` / `timestamp with time zone` |  |  |
| `total_claims` | `integer` / `integer` |  | default: `0` |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có | PK |

## `user_notification_reads`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `notification_id` | `string` / `uuid` |  | FK → `notifications.id` |
| `read_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` |  |  |

## `user_schedules`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `day_of_week` | `integer` / `smallint` | có |  |
| `end_time` | `string` / `time without time zone` | có |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `is_active` | `boolean` / `boolean` |  | default: `True` |
| `last_notified_at` | `string` / `timestamp with time zone` |  |  |
| `start_time` | `string` / `time without time zone` | có |  |
| `task_name` | `string` / `text` |  | default: `Học tập` |
| `updated_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_id` | `string` / `uuid` | có | FK → `profiles.id` |

## `user_sessions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `device_type` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `extensions.uuid_generate_v4()` |
| `ip_address` | `string` / `text` |  |  |
| `login_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `user_agent` | `string` / `text` |  |  |
| `user_id` | `string` / `uuid` | có |  |

## `vocabulary_sets`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `description` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `title` | `string` / `text` | có |  |
| `user_id` | `string` / `uuid` | có |  |

## `wallet_transactions`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `amount` | `integer` / `bigint` | có |  |
| `created_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `description` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `metadata` | `jsonb` |  |  |
| `reference_code` | `string` / `text` |  |  |
| `referral_code` | `string` / `text` |  |  |
| `status` | `string` / `text` | có | default: `pending` |
| `type` | `string` / `text` | có |  |
| `updated_at` | `string` / `timestamp with time zone` | có | default: `timezone('utc'::text, now())` |
| `user_id` | `string` / `uuid` | có |  |

## `words`

| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |
|-----|-------------------|----------|--------|
| `created_at` | `string` / `timestamp with time zone` |  | default: `now()` |
| `ease_factor` | `number` / `double precision` |  | default: `2.5` |
| `example_sentence_en` | `string` / `text` |  |  |
| `example_sentence_vi` | `string` / `text` |  |  |
| `id` | `string` / `uuid` | có | PK; default: `gen_random_uuid()` |
| `interval` | `integer` / `integer` |  | default: `0` |
| `last_reviewed` | `string` / `timestamp with time zone` |  |  |
| `meaning` | `string` / `text` | có |  |
| `next_review_date` | `string` / `timestamp with time zone` |  |  |
| `part_of_speech` | `string` / `text` |  |  |
| `set_id` | `string` / `uuid` | có | FK → `vocabulary_sets.id` |
| `term` | `string` / `text` | có |  |
| `uk_ipa` | `string` / `text` |  |  |
| `us_ipa` | `string` / `text` |  |  |
