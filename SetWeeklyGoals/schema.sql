use `weekly_goals`;

CREATE TABLE `users`
(
    `id`         int(11) NOT NULL AUTO_INCREMENT,
    `name`       varchar(255) NOT NULL,
    `created_at` datetime     NOT NULL,
    `updated_at` datetime     NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `goals`
(
    `id`          int(11) NOT NULL AUTO_INCREMENT,
    `user_id`     int(11) NOT NULL,
    `description` varchar(255) NOT NULL,
    `resolved`    tinyint(1) NOT NULL,
    `year`        int(11) NOT NULL,
    `month`       int(11) NOT NULL,
    `week`        int(11) NOT NULL,
    `created_at`  datetime     NOT NULL,
    `updated_at`  datetime     NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `assessments`
(
    `id`         int(11) NOT NULL AUTO_INCREMENT,
    `user_id`    int(11) NOT NULL,
    `year`       int(11) NOT NULL,
    `month`      int(11) NOT NULL,
    `week`       int(11) NOT NULL,
    `content`    text     NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

