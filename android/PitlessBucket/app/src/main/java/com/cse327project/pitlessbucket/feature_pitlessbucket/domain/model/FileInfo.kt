package com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model

import java.util.UUID
import java.util.Date

data class FileInfo(
    val uid: UUID,
    val firebaseUid: String,
    val fileName: String,
    val contentType: String,
    val extension: String,
    val size: Long,
    val createdAt: Date,
    val updatedAt: Date
)


