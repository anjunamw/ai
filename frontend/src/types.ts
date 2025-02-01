# frontend/src/types.ts
export interface Email {
    id: string;
    subject: string;
    from: string;
    body: string;
}
export interface JIRAIssue {
    id: string;
    key: string;
    summary: string;
    status: string;
}

export interface SmartHomeDevice {
    id: string;
    name: string;
    status: string;
}
export interface SocialMediaPost {
    id: string;
    text: string;
    created_at: string;
}
export interface TravelResult {
    id: string;
    destination: string;
    price: number;
}

export interface Note {
    id?: string;
    title: string;
    content: string;
}

export interface ToDoItem {
    id?: string;
    description: string;
    priority_user_set: string;
}