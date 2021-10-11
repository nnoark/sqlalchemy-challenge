CREATE TABLE "stations" (
    "station" VARCHAR(255)   NOT NULL,
    "name" VARCHAR(255)   NOT NULL,
	"latitude" DECIMAL NOT NULL,
	"longitude" DECIMAL NOT NULL,
	"elevation" DECIMAL NOT NULL,
    CONSTRAINT "pk_stations" PRIMARY KEY (
        "station"
     )
);

CREATE TABLE "measurements" (
    "station" VARCHAR(255)   NOT NULL,
    "date" DATE NOT NULL,
    "prcp" DECIMAL   NOT NULL,
    "tobs" INTEGER   NOT NULL,
    CONSTRAINT "pk_measurements" PRIMARY KEY (
        "date"
     )
);

ALTER TABLE "measurements" ADD CONSTRAINT "fk_measurements" FOREIGN KEY("station")
REFERENCES "stations" ("station");

ALTER TABLE "measurements" ALTER COLUMN "prcp" drop not null;
ALTER TABLE "measurements" DROP CONSTRAINT "pk_measurements"
ALTER TABLE "measurements" DROP CONSTRAINT "fk_measurements"
ALTER TABLE "stations" DROP CONSTRAINT "pk_stations"
ALTER TABLE "measurements" ADD COLUMN "id" SERIAL NOT NULL
ALTER TABLE "stations" ADD COLUMN "id" SERIAL NOT NULL
ALTER TABLE "measurements" ADD CONSTRAINT "pk_measurements" PRIMARY KEY ("id")
ALTER TABLE "stations" ADD CONSTRAINT "pk_stations" PRIMARY KEY ("id")
alter table "measurements" alter column "date" type varchar(255)

