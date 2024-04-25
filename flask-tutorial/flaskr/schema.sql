DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS survey_instances;
DROP TABLE IF EXISTS constructs;
DROP TABLE IF EXISTS survey_datapoints;
DROP TABLE IF EXISTS questions;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE survey_instances (
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  instance_name TEXT NOT NULL,
  quarter TEXT NOT NULL,
  year TEXT NOT NULL,
  PRIMARY KEY (quarter, year)
);

CREATE TABLE constructs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  construct_name TEXT NOT NULL UNIQUE
);

INSERT INTO constructs(construct_name) VALUES ('practice_question');
INSERT INTO constructs(construct_name) VALUES ('culture');
INSERT INTO constructs(construct_name) VALUES ('dev_systems');
INSERT INTO constructs(construct_name) VALUES ('work_sharing');
INSERT INTO constructs(construct_name) VALUES ('runtime_envs');
INSERT INTO constructs(construct_name) VALUES ('knowledge_management');

CREATE TABLE questions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_name TEXT NOT NULL UNIQUE,
  construct_id INTEGER NOT NULL,
  FOREIGN KEY (construct_id) REFERENCES construct (id)
);

INSERT INTO questions(question_name, construct_id) SELECT 'will_complete', id FROM constructs WHERE construct_name='practice_question';
INSERT INTO questions(question_name, construct_id) SELECT 'fail_learn_opportunity', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'responsibility_shared', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'collab_rewarded', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'ideas_welcomed', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'info_sought', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'failures_shame_free', id FROM constructs WHERE construct_name='culture';
INSERT INTO questions(question_name, construct_id) SELECT 'scm_works', id FROM constructs WHERE construct_name='dev_systems';
INSERT INTO questions(question_name, construct_id) SELECT 'task_runners_work', id FROM constructs WHERE construct_name='dev_systems';
INSERT INTO questions(question_name, construct_id) SELECT 'artifact_managment_works', id FROM constructs WHERE construct_name='dev_systems';
INSERT INTO questions(question_name, construct_id) SELECT 'integration_is_simple', id FROM constructs WHERE construct_name='work_sharing';
INSERT INTO questions(question_name, construct_id) SELECT 'changes_simple_safe', id FROM constructs WHERE construct_name='work_sharing';
INSERT INTO questions(question_name, construct_id) SELECT 'changes_distinct', id FROM constructs WHERE construct_name='work_sharing';
INSERT INTO questions(question_name, construct_id) SELECT 'changes_clear', id FROM constructs WHERE construct_name='work_sharing';
INSERT INTO questions(question_name, construct_id) SELECT 'releases_simple', id FROM constructs WHERE construct_name='work_sharing';
INSERT INTO questions(question_name, construct_id) SELECT 'env_cfg_easy', id FROM constructs WHERE construct_name='runtime_envs';
INSERT INTO questions(question_name, construct_id) SELECT 'env_startup_easy', id FROM constructs WHERE construct_name='runtime_envs';
INSERT INTO questions(question_name, construct_id) SELECT 'resources_available', id FROM constructs WHERE construct_name='runtime_envs';
INSERT INTO questions(question_name, construct_id) SELECT 'safe_experimental_envs', id FROM constructs WHERE construct_name='runtime_envs';
INSERT INTO questions(question_name, construct_id) SELECT 'easy_experimental_envs', id FROM constructs WHERE construct_name='runtime_envs';
INSERT INTO questions(question_name, construct_id) SELECT 'policies_clear', id FROM constructs WHERE construct_name='knowledge_management';
INSERT INTO questions(question_name, construct_id) SELECT 'policies_usable', id FROM constructs WHERE construct_name='knowledge_management';
INSERT INTO questions(question_name, construct_id) SELECT 'policies_discoverable', id FROM constructs WHERE construct_name='knowledge_management';
INSERT INTO questions(question_name, construct_id) SELECT 'policies_meaningful', id FROM constructs WHERE construct_name='knowledge_management';

CREATE TABLE survey_datapoints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  response_timestamp TIMESTAMP NOT NULL,
  survey_instance int NOT NULL,
  will_complete int NOT NULL,
  fail_learn_opportunity int NOT NULL,
  responsibility_shared int NOT NULL,
  collab_rewarded int NOT NULL,
  ideas_welcomed int NOT NULL,
  info_sought int NOT NULL,
  failures_shame_free int NOT NULL,
  scm_works int NOT NULL,
  task_runners_work int NOT NULL,
  artifact_managment_works int NOT NULL,
  integration_is_simple int NOT NULL,
  changes_simple_safe int NOT NULL,
  changes_distinct int NOT NULL,
  changes_clear int NOT NULL,
  releases_simple int NOT NULL,
  env_cfg_easy int NOT NULL,
  env_startup_easy int NOT NULL,
  resources_available int NOT NULL,
  safe_experimental_envs int NOT NULL,
  easy_experimental_envs int NOT NULL,
  policies_clear int NOT NULL,
  policies_usable int NOT NULL,
  policies_discoverable int NOT NULL,
  policies_meaningful int NOT NULL,

  CHECK (will_complete IN(1, 2, 3, 4, 5)),
  CHECK (fail_learn_opportunity IN(1, 2, 3, 4, 5)),
  CHECK (responsibility_shared IN(1, 2, 3, 4, 5)),
  CHECK (collab_rewarded IN(1, 2, 3, 4, 5)),
  CHECK (ideas_welcomed IN(1, 2, 3, 4, 5)),
  CHECK (info_sought IN(1, 2, 3, 4, 5)),
  CHECK (failures_shame_free IN(1, 2, 3, 4, 5)),
  CHECK (scm_works IN(1, 2, 3, 4, 5)),
  CHECK (task_runners_work IN(1, 2, 3, 4, 5)),
  CHECK (artifact_managment_works IN(1, 2, 3, 4, 5)),
  CHECK (integration_is_simple IN(1, 2, 3, 4, 5)),
  CHECK (changes_simple_safe IN(1, 2, 3, 4, 5)),
  CHECK (changes_distinct IN(1, 2, 3, 4, 5)),
  CHECK (changes_clear IN(1, 2, 3, 4, 5)),
  CHECK (releases_simple IN(1, 2, 3, 4, 5)),
  CHECK (env_cfg_easy IN(1, 2, 3, 4, 5)),
  CHECK (env_startup_easy IN(1, 2, 3, 4, 5)),
  CHECK (resources_available IN(1, 2, 3, 4, 5)),
  CHECK (safe_experimental_envs IN(1, 2, 3, 4, 5)),
  CHECK (easy_experimental_envs IN(1, 2, 3, 4, 5)),
  CHECK (policies_clear IN(1, 2, 3, 4, 5)),
  CHECK (policies_usable IN(1, 2, 3, 4, 5)),
  CHECK (policies_discoverable IN(1, 2, 3, 4, 5)),
  CHECK (policies_meaningful IN(1, 2, 3, 4, 5)),

  FOREIGN KEY (survey_instance) REFERENCES survey_instances,
  FOREIGN KEY (will_complete) REFERENCES question(construct_name),
  FOREIGN KEY (fail_learn_opportunity) REFERENCES question(construct_name),
  FOREIGN KEY (responsibility_shared) REFERENCES question(construct_name),
  FOREIGN KEY (collab_rewarded) REFERENCES question(construct_name),
  FOREIGN KEY (ideas_welcomed) REFERENCES question(construct_name),
  FOREIGN KEY (info_sought) REFERENCES question(construct_name),
  FOREIGN KEY (failures_shame_free) REFERENCES question(construct_name),
  FOREIGN KEY (scm_works) REFERENCES question(construct_name),
  FOREIGN KEY (task_runners_work) REFERENCES question(construct_name),
  FOREIGN KEY (artifact_managment_works) REFERENCES question(construct_name),
  FOREIGN KEY (integration_is_simple) REFERENCES question(construct_name),
  FOREIGN KEY (changes_simple_safe) REFERENCES question(construct_name),
  FOREIGN KEY (changes_distinct) REFERENCES question(construct_name),
  FOREIGN KEY (changes_clear) REFERENCES question(construct_name),
  FOREIGN KEY (releases_simple) REFERENCES question(construct_name),
  FOREIGN KEY (env_cfg_easy) REFERENCES question(construct_name),
  FOREIGN KEY (env_startup_easy) REFERENCES question(construct_name),
  FOREIGN KEY (resources_available) REFERENCES question(construct_name),
  FOREIGN KEY (safe_experimental_envs) REFERENCES question(construct_name),
  FOREIGN KEY (easy_experimental_envs) REFERENCES question(construct_name),
  FOREIGN KEY (policies_clear) REFERENCES question(construct_name),
  FOREIGN KEY (policies_usable) REFERENCES question(construct_name),
  FOREIGN KEY (policies_discoverable) REFERENCES question(construct_name),
  FOREIGN KEY (policies_meaningful) REFERENCES question(construct_name)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
