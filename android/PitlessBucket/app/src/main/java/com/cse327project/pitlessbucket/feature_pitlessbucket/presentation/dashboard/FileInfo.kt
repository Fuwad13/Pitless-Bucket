package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard

import java.util.UUID
import java.util.Date

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


