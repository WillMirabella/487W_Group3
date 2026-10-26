import { getCarById } from './db';

class Car {
    make: string;
    model: string;
    color: string;
    year: number;
    capacity: number;

    constructor(id: string) {
        let row = getCarById(id);
        
        if (!row) {
            throw new Error(`Car with ID ${id} not found.`);
        }
        
        this.make = row[0];
        this.model = row[1];
        this.color = row[2];
        this.year = row[3];
        this.capacity = row[4];
    }
}