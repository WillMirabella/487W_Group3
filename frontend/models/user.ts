import { getUserById } from "./db";

class User {
    firstName: string;
    lastName: string;
    phone: string;
    email: string;
    gender: string;
    description: string;
    gradYear: number;
    major: string;
    schedule: [number, number];
    address: string;
    preferredPayment: string;
    carId: string;

    constructor(id: string) {
        let row = getUserById(id);
        
        if (!row) {
            throw new Error(`User with ID ${id} not found.`);
        }
        
        this.firstName = row[0];
        this.lastName = row[1];
        this.phone = row[2];
        this.email = row[3];
        this.gender = row[4];
        this.description = row[5];
        this.gradYear = row[6];
        this.major = row[7];
        this.schedule = row[8];
        this.address = row[9];
        this.preferredPayment = row[10];
        this.carId = row[11];
    }
}
