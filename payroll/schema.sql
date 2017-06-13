DROP OWNED BY guest;

create table if not exists job (
    type varchar(40) primary key,
    rank int,
    base_salary int not null
);

create table if not exists info (
    uid int primary key check ( uid >= 1000),
    pw varchar(40) not null,
    name varchar(40) not null,
    email varchar(40) not null check ( email like '%@%.%'),
    job varchar(40) not null references job(type),
    dept varchar(40),
    is_admin boolean default false
);

create table if not exists attendance (
    uid int references info(uid),
    day date,
    primary key (uid, day)
);

create table if not exists allowance (
    uid int references info(uid),
    day date,
    hour int,
    type int,
    bounty int,
    primary key (uid, day)
);

create table if not exists salary (
    uid int references info(uid),
    month date,
    salary int,
    primary key (uid, month)
);


-- table job
insert into job(type, rank, base_salary) values('Chairman', 0, 10000);
insert into job(type, rank, base_salary) values('GManager', 1, 8000);
insert into job(type, rank, base_salary) values('Financer', 1, 8000);
insert into job(type, rank, base_salary) values('ManagerA', 2, 7000);
insert into job(type, rank, base_salary) values('ManagerB', 2, 7000);
insert into job(type, rank, base_salary) values('ManagerC', 2, 7000);
insert into job(type, rank, base_salary) values('Expert', 2, 8000);
insert into job(type, rank, base_salary) values('SeniorStaff', 3, 6000);
insert into job(type, rank, base_salary) values('MidderStaff', 4, 5000);
insert into job(type, rank, base_salary) values('PrimaryStaff', 5, 4000);
insert into job(type, rank, base_salary) values('Trainee', 6, 3000);


-- table info
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1000, 'nwp_pw', 'nieweiping', 'nieweiping@go.com', 'Chairman', TRUE, null);
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1001, 'yb_pw', 'yubing', 'yubing@go.com', 'GManager',TRUE, null);
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1002, 'wrn_pw', 'wangrunan', 'wangrunan@go.com', 'Financer',TRUE, null);

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1003, 'kj_pw', 'kejie', 'kejie@go.com', 'ManagerA',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1004, 'gl_pw', 'guli', 'guli@go.com', 'ManagerB',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1005, 'twx_pw', 'tangweixing', 'tangweixing@go.com', 'ManagerC',TRUE, 'C');

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1006, 'cyy_pw', 'chenyaoye', 'chenyaoye@go.com', 'Expert',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1007, 'tjj_pw', 'tuojiaxi', 'tuojiaxi@go.com', 'Expert',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1008, 'zrr_pw', 'zhouruiyang', 'zhouruiyang@go.com', 'Expert',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1009, 'sy_pw', 'shiyue', 'shiyue@go.com', 'Expert',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1010, 'myt_pw', 'miyuting', 'miyuting@go.com', 'Expert',TRUE, 'C');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1011, 'jwj_pw', 'jiangweijie', 'jiangweijie@go.com', 'Expert',TRUE, 'C');

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1012, 'dyf_pw', 'dangyifei', 'dangyifei@go.com', 'SeniorStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1013, 'pwy_pw', 'piaowenyao', 'piaowenyao@go.com', 'SeniorStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1014, 'lqc_pw', 'liqincheng', 'liqincheng@go.com', 'SeniorStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1015, 'lx_pw', 'lianxiao', 'lianxiao@go.com', 'SeniorStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1016, 'fty_pw', 'fantingyu', 'fantingyu@go.com', 'SeniorStaff',TRUE, 'C');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1017, 'fyr_pw', 'fanyunruo', 'fanyunruo@go.com', 'SeniorStaff',TRUE, 'C');

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1018, 'yzy_pw', 'yuzhiying', 'yuzhiying@go.com', 'MidderStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1019, 'wcx_pw', 'wangchenxing', 'wangchenxing@go.com', 'MidderStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1020, 'rnw_pw', 'ruinaiwei', 'ruinaiwei@go.com', 'MidderStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1021, 'lj_pw', 'lujia', 'lujia@go.com', 'MidderStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1022, 'lh_pw', 'lihe', 'lihe@go.com', 'MidderStaff',TRUE, 'C');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1023, 'srh_pw', 'songronghui', 'songronghui@go.com', 'MidderStaff',TRUE, 'C');

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1024, 'ydx_pw', 'yangdingxin', 'yangdingxing@go.com', 'PrimaryStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1025, 'ply_pw', 'pengliyao', 'pengliyao@go.com', 'PrimaryStaff',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1026, 'pq_pw', 'pengquan', 'pengquan@go.com', 'PrimaryStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1027, 'ch_pw', 'changhao', 'changhao@go.com', 'PrimaryStaff',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1028, 'kj_pw', 'kongjie', 'kongjie@go.com', 'PrimaryStaff',TRUE, 'C');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1029, 'gly_pw', 'gulingyi', 'gulingyi@go.com', 'PrimaryStaff',TRUE, 'C');

insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1030, 'gzh_pw', 'guzihao', 'guzihao@go.com', 'Trainee',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1031, 'hys_pw', 'huangyunsong', 'huangyunsong@go.com', 'Trainee',TRUE, 'A');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1032, 'zcy_pw', 'zhaochengyu', 'zhaochengyu@go.com', 'Trainee',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1033, 'txy_pw', 'tuxiaoyu', 'tuxiaoyu@go.com', 'Trainee',TRUE, 'B');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1034, 'xeh_pw', 'xieerhao', 'xieerhao@go.com', 'Trainee',TRUE, 'C');
insert into info(uid, pw, name, email, job, is_admin, dept)
	values(1035, 'gyz_pw', 'guoyuzheng', 'guoyuzheng@go.com', 'Trainee',TRUE, 'C');


-- table attendance
insert into attendance(uid, day) values(1000, '2017-01-01');
insert into attendance(uid, day) values(1000, '2017-01-02');
insert into attendance(uid, day) values(1000, '2017-01-03');
insert into attendance(uid, day) values(1000, '2017-01-04');
insert into attendance(uid, day) values(1000, '2017-01-05');
insert into attendance(uid, day) values(1000, '2017-01-06');
insert into attendance(uid, day) values(1000, '2017-01-07');
insert into attendance(uid, day) values(1000, '2017-01-08');
insert into attendance(uid, day) values(1000, '2017-01-09');
insert into attendance(uid, day) values(1000, '2017-01-10');
insert into attendance(uid, day) values(1000, '2017-01-11');
insert into attendance(uid, day) values(1000, '2017-01-12');
insert into attendance(uid, day) values(1000, '2017-01-13');
insert into attendance(uid, day) values(1000, '2017-01-14');
insert into attendance(uid, day) values(1000, '2017-01-15');
insert into attendance(uid, day) values(1000, '2017-01-16');
insert into attendance(uid, day) values(1000, '2017-01-17');
insert into attendance(uid, day) values(1000, '2017-01-18');
insert into attendance(uid, day) values(1000, '2017-01-19');
insert into attendance(uid, day) values(1000, '2017-01-20');
insert into attendance(uid, day) values(1000, '2017-01-21');
insert into attendance(uid, day) values(1000, '2017-01-22');
insert into attendance(uid, day) values(1000, '2017-01-23');
insert into attendance(uid, day) values(1000, '2017-01-24');
insert into attendance(uid, day) values(1000, '2017-01-25');
insert into attendance(uid, day) values(1000, '2017-01-26');
insert into attendance(uid, day) values(1000, '2017-01-27');
insert into attendance(uid, day) values(1000, '2017-01-28');
insert into attendance(uid, day) values(1000, '2017-01-29');
insert into attendance(uid, day) values(1000, '2017-01-30');
insert into attendance(uid, day) values(1000, '2017-01-31');
insert into attendance(uid, day) values(1001, '2017-01-01');
insert into attendance(uid, day) values(1001, '2017-01-02');
insert into attendance(uid, day) values(1001, '2017-01-03');
insert into attendance(uid, day) values(1001, '2017-01-04');
insert into attendance(uid, day) values(1001, '2017-01-05');
insert into attendance(uid, day) values(1001, '2017-01-06');
insert into attendance(uid, day) values(1001, '2017-01-07');
insert into attendance(uid, day) values(1001, '2017-01-08');
insert into attendance(uid, day) values(1001, '2017-01-09');
insert into attendance(uid, day) values(1001, '2017-01-10');
insert into attendance(uid, day) values(1001, '2017-01-11');
insert into attendance(uid, day) values(1001, '2017-01-12');
insert into attendance(uid, day) values(1001, '2017-01-13');
insert into attendance(uid, day) values(1001, '2017-01-14');
insert into attendance(uid, day) values(1001, '2017-01-15');
insert into attendance(uid, day) values(1001, '2017-01-16');
insert into attendance(uid, day) values(1001, '2017-01-17');
insert into attendance(uid, day) values(1001, '2017-01-18');
insert into attendance(uid, day) values(1001, '2017-01-19');
insert into attendance(uid, day) values(1001, '2017-01-20');
insert into attendance(uid, day) values(1001, '2017-01-21');
insert into attendance(uid, day) values(1001, '2017-01-22');
-- not 23 24
insert into attendance(uid, day) values(1001, '2017-01-25');
insert into attendance(uid, day) values(1001, '2017-01-26');
insert into attendance(uid, day) values(1001, '2017-01-27');
insert into attendance(uid, day) values(1001, '2017-01-28');
insert into attendance(uid, day) values(1001, '2017-01-29');
insert into attendance(uid, day) values(1001, '2017-01-30');
insert into attendance(uid, day) values(1001, '2017-01-31');


-- table allowance
-- type 0 100
-- type 1 70
-- type 2 60
-- type 3 50
-- type 4 40
insert into allowance(uid, day, hour, type, bounty) values(1000, '2017-01-02', 2, 4, 80);
insert into allowance(uid, day, hour, type, bounty) values(1000, '2017-01-06', 2, 4, 80);
insert into allowance(uid, day, hour, type, bounty) values(1001, '2017-01-02', 3, 4, 120);
insert into allowance(uid, day, hour, type, bounty) values(1001, '2017-01-05', 1, 4, 40);
insert into allowance(uid, day, hour, type, bounty) values(1003, '2017-01-02', 2, 4, 80);
insert into allowance(uid, day, hour, type, bounty) values(1003, '2017-01-07', 2, 4, 80);
insert into allowance(uid, day, hour, type, bounty) values(1003, '2017-01-08', 2, 4, 80);
insert into allowance(uid, day, hour, type, bounty) values(1003, '2017-01-09', 3, 4, 120);
insert into allowance(uid, day, hour, type, bounty) values(1006, '2017-01-02', 3, 4, 120);
insert into allowance(uid, day, hour, type, bounty) values(1008, '2017-01-02', 3, 4, 120);
insert into allowance(uid, day, hour, type, bounty) values(1009, '2017-01-02', 3, 4, 120);


-- table salary
insert into salary(uid, month, salary) values(1000, '2016-12-31', 10200);
insert into salary(uid, month, salary) values(1001, '2016-12-31', 10100);
insert into salary(uid, month, salary) values(1002, '2016-12-31', 8000);
insert into salary(uid, month, salary) values(1003, '2016-12-31', 7500);
insert into salary(uid, month, salary) values(1004, '2016-12-31', 9000);
insert into salary(uid, month, salary) values(1005, '2016-12-31', 8800);
insert into salary(uid, month, salary) values(1006, '2016-12-31', 7600);
insert into salary(uid, month, salary) values(1007, '2016-12-31', 7000);
insert into salary(uid, month, salary) values(1008, '2016-12-31', 6800);
insert into salary(uid, month, salary) values(1009, '2016-12-31', 7030);
insert into salary(uid, month, salary) values(1010, '2016-12-31', 6800);
