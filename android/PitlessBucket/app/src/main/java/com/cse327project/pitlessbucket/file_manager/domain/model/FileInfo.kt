package com.cse327project.pitlessbucket.file_manager.domain.model

import java.util.UUID

data class FileInfo(
    val uid: UUID,
    val firebase_uid: String,
    val file_name: String,
    val content_type: String,
    val extension: String,
    val size: Long,
    val created_at: String,
    val updated_at: String
)


